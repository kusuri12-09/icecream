import json
import shutil
import tempfile
from pathlib import Path

import pytest

from app.services import diagnosis_engine


def test_reload_criteria_applies_valid_revision(monkeypatch):
    with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp_dir:
        criteria_path = Path(temp_dir) / "fitness_grade_criteria.json"
        shutil.copyfile(diagnosis_engine.CRITERIA_PATH, criteria_path)
        monkeypatch.setattr(diagnosis_engine, "CRITERIA_PATH", criteria_path)
        diagnosis_engine.load_criteria.cache_clear()

        try:
            original = diagnosis_engine.load_criteria()
            revised = json.loads(criteria_path.read_text(encoding="utf-8"))
            revised["meta"]["version"] = "test-revision"
            criteria_path.write_text(json.dumps(revised), encoding="utf-8")

            loaded = diagnosis_engine.reload_criteria()

            assert original["meta"]["version"] != loaded["meta"]["version"]
            assert loaded["meta"]["version"] == "test-revision"
        finally:
            diagnosis_engine.load_criteria.cache_clear()


def test_reload_criteria_keeps_previous_cache_when_revision_is_invalid(monkeypatch):
    with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp_dir:
        criteria_path = Path(temp_dir) / "fitness_grade_criteria.json"
        shutil.copyfile(diagnosis_engine.CRITERIA_PATH, criteria_path)
        monkeypatch.setattr(diagnosis_engine, "CRITERIA_PATH", criteria_path)
        diagnosis_engine.load_criteria.cache_clear()

        try:
            cached = diagnosis_engine.load_criteria()
            criteria_path.write_text("{}", encoding="utf-8")

            with pytest.raises(diagnosis_engine.CriteriaValidationError):
                diagnosis_engine.reload_criteria()

            assert diagnosis_engine.load_criteria()["meta"]["version"] == cached["meta"]["version"]
        finally:
            diagnosis_engine.load_criteria.cache_clear()


def test_validate_criteria_rejects_invalid_grade_rule_type():
    criteria = json.loads(diagnosis_engine.CRITERIA_PATH.read_text(encoding="utf-8"))
    criteria["gradeRules"]["fruit"] = []

    with pytest.raises(diagnosis_engine.CriteriaValidationError, match="등급 규칙 형식"):
        diagnosis_engine.validate_criteria(criteria)


def test_validate_criteria_rejects_required_item_outside_api_contract():
    criteria = json.loads(diagnosis_engine.CRITERIA_PATH.read_text(encoding="utf-8"))
    criteria["gradeRules"]["fruit"]["requiredItems"] = ["unknown"]

    with pytest.raises(diagnosis_engine.CriteriaValidationError, match="requiredItems"):
        diagnosis_engine.validate_criteria(criteria)
