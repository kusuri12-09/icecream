import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from app.core.config import CRITERIA_PATH


GRADE_ORDER = ("fruit", "flower", "sprout")
API_GRADES = {"fruit": "FRUIT", "flower": "FLOWER", "sprout": "SPROUT", "seed": "SEED"}
API_ITEMS = {
    "CARDIO": "cardio",
    "GRIP": "grip",
    "MUSCULAR_END": "muscularEnd",
    "FLEXIBILITY": "flexibility",
    "AGILITY": "agility",
    "POWER": "power",
    "COORDINATION": "coordination",
    "BMI": "bmi",
}
REQUIRED_GENDERS = ("male", "female")
VALID_DIRECTIONS = {"higher", "lower"}


@dataclass(frozen=True)
class DiagnosisResult:
    grade: str
    item_grades: dict[str, str | None]
    strengths: list[str]
    weaknesses: list[str]
    undecidable_grades: list[str]


class CriteriaValidationError(ValueError):
    """기준표가 진단 엔진 계약을 만족하지 않을 때 발생한다."""


def _read_criteria() -> dict[str, Any]:
    try:
        criteria = json.loads(CRITERIA_PATH.read_text(encoding="utf-8"))
    except OSError as exc:
        raise CriteriaValidationError(f"기준표 파일을 읽을 수 없습니다: {CRITERIA_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise CriteriaValidationError(f"기준표 JSON 형식이 올바르지 않습니다: {CRITERIA_PATH}") from exc

    validate_criteria(criteria)
    return criteria


def validate_criteria(criteria: Any) -> None:
    """진단에 필요한 기준표 구조와 값의 존재 여부를 검증한다."""
    if not isinstance(criteria, dict):
        raise CriteriaValidationError("기준표 최상위 값은 객체여야 합니다.")

    meta = criteria.get("meta")
    items = criteria.get("items")
    grade_rules = criteria.get("gradeRules")
    thresholds = criteria.get("thresholds")
    if not isinstance(meta, dict) or not meta.get("version"):
        raise CriteriaValidationError("기준표 meta.version이 필요합니다.")
    if not isinstance(items, dict) or set(API_ITEMS.values()) - set(items):
        raise CriteriaValidationError("기준표에 진단 항목 정의가 누락되었습니다.")
    if not isinstance(grade_rules, dict) or any(grade not in grade_rules for grade in GRADE_ORDER):
        raise CriteriaValidationError("기준표 등급 규칙이 누락되었습니다.")
    if not isinstance(thresholds, dict):
        raise CriteriaValidationError("기준표 thresholds가 필요합니다.")

    for item_key in API_ITEMS.values():
        item = items[item_key]
        if not isinstance(item, dict) or item.get("direction") not in VALID_DIRECTIONS:
            raise CriteriaValidationError(f"기준표 항목 방향성이 올바르지 않습니다: {item_key}")

    expected_bands: set[str] | None = None
    for grade in GRADE_ORDER:
        grade_rule = grade_rules[grade]
        if not isinstance(grade_rule, dict):
            raise CriteriaValidationError(f"기준표 {grade} 등급 규칙 형식이 올바르지 않습니다.")
        required_items = grade_rule.get("requiredItems")
        if not isinstance(required_items, list) or any(item not in API_ITEMS.values() for item in required_items):
            raise CriteriaValidationError(f"기준표 {grade} 등급의 requiredItems가 올바르지 않습니다.")
        grade_thresholds = thresholds.get(grade)
        if not isinstance(grade_thresholds, dict):
            raise CriteriaValidationError(f"기준표 {grade} 등급의 thresholds가 누락되었습니다.")
        for gender in REQUIRED_GENDERS:
            bands = grade_thresholds.get(gender)
            if not isinstance(bands, dict) or not bands:
                raise CriteriaValidationError(f"기준표 {grade}/{gender} 연령대가 누락되었습니다.")
            band_keys = set(bands)
            if expected_bands is None:
                expected_bands = band_keys
            elif band_keys != expected_bands:
                raise CriteriaValidationError("기준표 등급별 연령대 구간이 일치하지 않습니다.")
            for band, values in bands.items():
                if not isinstance(values, dict):
                    raise CriteriaValidationError(f"기준표 임계값 형식이 올바르지 않습니다: {grade}/{gender}/{band}")
                missing_items = [item for item in required_items if item not in values]
                if missing_items:
                    raise CriteriaValidationError(
                        f"기준표 임계값이 누락되었습니다: {grade}/{gender}/{band}/{missing_items}"
                    )
                try:
                    for item in values.values():
                        float(item)
                except (TypeError, ValueError) as exc:
                    raise CriteriaValidationError(f"기준표 임계값은 숫자여야 합니다: {grade}/{gender}/{band}") from exc


@lru_cache
def load_criteria() -> dict[str, Any]:
    return _read_criteria()


def reload_criteria() -> dict[str, Any]:
    """개정 기준표를 검증한 뒤 캐시를 비우고 다음 진단부터 다시 로드한다."""
    _read_criteria()
    load_criteria.cache_clear()
    return load_criteria()


def age_band(months: int, criteria: dict[str, Any] | None = None) -> str:
    criteria = criteria or load_criteria()
    for band in criteria["thresholds"]["fruit"]["male"]:
        start, end = (int(value) for value in band.split("-"))
        if start <= months <= end:
            return band
    raise ValueError("진단 대상 개월 수는 48~83개월이어야 합니다.")


def _passes(item_key: str, value: float, threshold: float, direction: str) -> bool:
    if item_key == "bmi":
        return value < threshold
    return value >= threshold if direction == "higher" else value <= threshold


def judge(gender: str, months: int, values: dict[str, float]) -> DiagnosisResult:
    criteria = load_criteria()
    band = age_band(months, criteria)
    gender_key = gender.lower()
    normalized = {API_ITEMS.get(key, key): value for key, value in values.items()}
    item_grades: dict[str, str | None] = {}
    for api_key, item_key in API_ITEMS.items():
        value = normalized.get(item_key)
        if value is None:
            item_grades[api_key] = None
            continue
        item_info = criteria["items"][item_key]
        grade = "seed"
        for grade_key in GRADE_ORDER:
            threshold = criteria["thresholds"][grade_key][gender_key][band].get(item_key)
            if threshold is not None and _passes(item_key, float(value), float(threshold), item_info["direction"]):
                grade = grade_key
                break
        item_grades[api_key] = API_GRADES[grade]

    undecidable: list[str] = []
    overall = "SEED"
    for grade_key in GRADE_ORDER:
        required = criteria["gradeRules"][grade_key]["requiredItems"]
        missing = [item for item in required if item not in normalized]
        if missing:
            undecidable.append(API_GRADES[grade_key])
            continue
        thresholds = criteria["thresholds"][grade_key][gender_key][band]
        if all(_passes(item, float(normalized[item]), float(thresholds[item]), criteria["items"][item]["direction"]) for item in required):
            overall = API_GRADES[grade_key]
            break

    strengths = [key for key, grade in item_grades.items() if key != "BMI" and grade == overall]
    weaknesses = [key for key, grade in item_grades.items() if key != "BMI" and grade == "SEED"]
    return DiagnosisResult(overall, item_grades, strengths, weaknesses, undecidable)
