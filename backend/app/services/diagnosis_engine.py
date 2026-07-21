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


@dataclass(frozen=True)
class DiagnosisResult:
    grade: str
    item_grades: dict[str, str | None]
    strengths: list[str]
    weaknesses: list[str]
    undecidable_grades: list[str]


@lru_cache
def load_criteria() -> dict[str, Any]:
    return json.loads(CRITERIA_PATH.read_text(encoding="utf-8"))


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
