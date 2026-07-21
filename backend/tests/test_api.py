import os

os.environ["DATABASE_URL"] = "sqlite:///./test.sqlite3"
os.environ["JWT_SECRET_KEY"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from app.db import Base, engine
from app.main import app
from app.services.diagnosis_engine import judge


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_diagnosis_fruit_at_threshold():
    values = {
        "CARDIO": 63,
        "GRIP": 53.8,
        "MUSCULAR_END": 9,
        "FLEXIBILITY": 12,
        "AGILITY": 9.46,
        "POWER": 105,
        "COORDINATION": 23.21,
    }
    result = judge("MALE", 62, values)
    assert result.grade == "FRUIT"
    assert result.weaknesses == []


def test_diagnosis_bmi_is_strict_and_missing_motor_items_are_undecidable():
    values = {"CARDIO": 31, "GRIP": 41.7, "MUSCULAR_END": 1, "FLEXIBILITY": 7, "BMI": 19.2}
    result = judge("MALE", 62, values)
    assert result.grade == "SEED"
    assert result.undecidable_grades == ["FRUIT", "FLOWER"]
    assert result.item_grades["BMI"] == "SEED"


@pytest.mark.parametrize(
    ("gender", "values", "expected"),
    [
        ("MALE", {"CARDIO": 63, "GRIP": 53.8, "MUSCULAR_END": 9, "FLEXIBILITY": 12, "AGILITY": 9.46, "POWER": 105, "COORDINATION": 23.21}, "FRUIT"),
        ("FEMALE", {"CARDIO": 67, "GRIP": 48.9, "MUSCULAR_END": 8, "FLEXIBILITY": 14, "AGILITY": 10.31, "POWER": 95, "COORDINATION": 25.04}, "FRUIT"),
        ("MALE", {"CARDIO": 48, "GRIP": 47.4, "MUSCULAR_END": 5, "FLEXIBILITY": 10.1, "AGILITY": 10.12, "POWER": 95, "COORDINATION": 25.39}, "FLOWER"),
        ("FEMALE", {"CARDIO": 53, "GRIP": 42.8, "MUSCULAR_END": 3, "FLEXIBILITY": 12.3, "AGILITY": 10.81, "POWER": 88, "COORDINATION": 27.42}, "FLOWER"),
        ("MALE", {"CARDIO": 31, "GRIP": 41.7, "MUSCULAR_END": 1, "FLEXIBILITY": 7, "BMI": 19.19}, "SPROUT"),
        ("FEMALE", {"CARDIO": 39, "GRIP": 37.9, "MUSCULAR_END": 0, "FLEXIBILITY": 9.9, "BMI": 18.09}, "SPROUT"),
        ("MALE", {"CARDIO": 31, "GRIP": 41.7, "MUSCULAR_END": 1, "FLEXIBILITY": 7}, "SEED"),
        ("MALE", {"CARDIO": 63, "GRIP": 53.8, "MUSCULAR_END": 9, "FLEXIBILITY": 12, "AGILITY": 9.47, "POWER": 105, "COORDINATION": 23.21}, "FLOWER"),
        ("MALE", {"CARDIO": 62, "GRIP": 53.8, "MUSCULAR_END": 9, "FLEXIBILITY": 12, "AGILITY": 9.46, "POWER": 105, "COORDINATION": 23.21}, "FLOWER"),
        ("MALE", {"CARDIO": 31, "GRIP": 41.7, "MUSCULAR_END": 1, "FLEXIBILITY": 7, "BMI": 19.2}, "SEED"),
    ],
)
def test_diagnosis_regression_matrix(gender: str, values: dict[str, float], expected: str):
    assert judge(gender, 62, values).grade == expected


def test_diagnosis_rejects_age_outside_criteria():
    with pytest.raises(ValueError, match="48~83"):
        judge("MALE", 47, {"CARDIO": 1})


def test_auth_child_and_measurement_flow(client: TestClient):
    signup = client.post("/api/v1/auth/signup", json={"email": "test@example.com", "password": "password123"})
    assert signup.status_code == 201
    token = signup.json()["data"]["accessToken"]
    headers = {"Authorization": f"Bearer {token}"}

    child = client.post(
        "/api/v1/children",
        headers=headers,
        json={"nickname": "콩이", "gender": "MALE", "birthYearMonth": "2021-05"},
    )
    assert child.status_code == 201
    child_data = child.json()["data"]
    assert child_data["birthYearMonth"] == "2021-05"

    measurement = client.post(
        f"/api/v1/children/{child_data['id']}/measurements",
        headers=headers,
        json={
            "type": "OFFICIAL",
            "measuredAt": "2026-07-19",
            "items": [
                {"itemKey": "CARDIO", "value": 63},
                {"itemKey": "GRIP", "value": 53.8},
                {"itemKey": "MUSCULAR_END", "value": 9},
                {"itemKey": "FLEXIBILITY", "value": 12},
                {"itemKey": "AGILITY", "value": 9.46},
                {"itemKey": "POWER", "value": 105},
                {"itemKey": "COORDINATION", "value": 23.21},
            ],
        },
    )
    assert measurement.status_code == 201
    assert measurement.json()["data"]["grade"] == "FRUIT"

    listed = client.get(f"/api/v1/children/{child_data['id']}/measurements", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["totalElements"] == 1


def test_private_api_requires_bearer(client: TestClient):
    response = client.get("/api/v1/children")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTH_UNAUTHORIZED"
