import os
from datetime import date

os.environ["DATABASE_URL"] = "sqlite:///./test.sqlite3"
os.environ["DB_USER"] = ""
os.environ["DB_PASSWORD"] = ""
os.environ["JWT_SECRET_KEY"] = "test-secret"

import pytest
from sqlalchemy.exc import IntegrityError
from fastapi.testclient import TestClient

from app.db import Base, SessionLocal, engine
from app.core.config import get_settings
from app.core.security import create_access_token
from app.external.kspo_client import ActivityRecord, CenterRecord
from app.main import app
from app.models import ActivityVideo, Center, Parent
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


def test_child_birth_year_month_rejects_non_preschool_range(client: TestClient):
    headers = auth_headers(client, "birth-range@example.com")
    for birth_year_month in ("2018-12", f"{date.today().year}-01"):
        response = client.post(
            "/api/v1/children",
            headers=headers,
            json={"nickname": "범위 테스트", "gender": "MALE", "birthYearMonth": birth_year_month},
        )
        assert response.status_code == 422


def test_private_api_requires_bearer(client: TestClient):
    response = client.get("/api/v1/children")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTH_UNAUTHORIZED"


def auth_headers(client: TestClient, email: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/signup", json={"email": email, "password": "password123"})
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['data']['accessToken']}"}


def test_centers_return_not_found_when_cache_is_empty(client: TestClient):
    headers = auth_headers(client, "empty-centers@example.com")

    response = client.get("/api/v1/centers", headers=headers)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "CENTER_NOT_FOUND"


def test_center_rejects_blank_address():
    db = SessionLocal()
    db.add(Center(ext_center_id="blank-address", name="주소 없는 센터", address="   "))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()
    db.close()


def create_child(client: TestClient, headers: dict[str, str]) -> str:
    response = client.post(
        "/api/v1/children",
        headers=headers,
        json={"nickname": "콩이", "gender": "MALE", "birthYearMonth": "2021-05"},
    )
    assert response.status_code == 201
    return response.json()["data"]["id"]


def create_fruit_measurement(client: TestClient, headers: dict[str, str], child_id: str) -> str:
    response = client.post(
        f"/api/v1/children/{child_id}/measurements",
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
    assert response.status_code == 201
    return response.json()["data"]["id"]


def test_children_crud_and_measurement_ownership(client: TestClient):
    owner_headers = auth_headers(client, "crud@example.com")
    other_headers = auth_headers(client, "other@example.com")
    child_id = create_child(client, owner_headers)

    listed = client.get("/api/v1/children", headers=owner_headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["totalElements"] == 1

    updated = client.patch(
        f"/api/v1/children/{child_id}",
        headers=owner_headers,
        json={"nickname": "수정된 콩이"},
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["nickname"] == "수정된 콩이"

    denied = client.get(f"/api/v1/children/{child_id}", headers=other_headers)
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "CHILD_ACCESS_DENIED"

    measurement_id = create_fruit_measurement(client, owner_headers, child_id)
    deleted = client.delete(f"/api/v1/children/{child_id}", headers=owner_headers)
    assert deleted.status_code == 200
    assert client.get(f"/api/v1/children/{child_id}", headers=owner_headers).status_code == 404
    assert client.get(f"/api/v1/measurements/{measurement_id}", headers=owner_headers).status_code == 404


def test_measurement_detail_growth_and_delete(client: TestClient):
    headers = auth_headers(client, "measurement@example.com")
    child_id = create_child(client, headers)
    measurement_id = create_fruit_measurement(client, headers, child_id)

    detail = client.get(f"/api/v1/measurements/{measurement_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["profile"]["strengths"]

    growth = client.get(f"/api/v1/children/{child_id}/growth?itemKey=CARDIO", headers=headers)
    assert growth.status_code == 200
    assert growth.json()["data"]["series"][0]["itemKey"] == "CARDIO"
    assert growth.json()["data"]["series"][0]["points"][0]["type"] == "OFFICIAL"

    deleted = client.delete(f"/api/v1/measurements/{measurement_id}", headers=headers)
    assert deleted.status_code == 200
    assert client.get(f"/api/v1/measurements/{measurement_id}", headers=headers).status_code == 404


def test_full_parent_diagnosis_history_and_insight_flow(client: TestClient):
    headers = auth_headers(client, "full-flow@example.com")
    db = SessionLocal()
    db.add_all(
        [
            Center(ext_center_id="flow-center-seoul", name="서울 센터", address="서울 강남구 테헤란로 1", sido_sigungu="서울 강남구", measure_count=12),
            Center(ext_center_id="flow-center-busan", name="부산 센터", address="부산 해운대구 센텀로 1", sido_sigungu="부산 해운대구", measure_count=4),
        ]
    )
    db.commit()
    db.close()

    child_id = create_child(client, headers)
    measurement_id = create_fruit_measurement(client, headers, child_id)

    detail = client.get(f"/api/v1/measurements/{measurement_id}", headers=headers)
    history = client.get(f"/api/v1/children/{child_id}/measurements", headers=headers)
    insight = client.get("/api/v1/insights/regional?sidoSigungu=서울%20강남구", headers=headers)

    assert detail.status_code == 200
    assert detail.json()["data"]["grade"] == "FRUIT"
    assert history.status_code == 200
    assert history.json()["data"]["totalElements"] == 1
    assert insight.status_code == 200
    assert insight.json()["data"]["regionMeasureCount"] == 12


def test_measurement_creation_rejects_invalid_age_and_duplicate_items(client: TestClient):
    headers = auth_headers(client, "invalid-measurement@example.com")
    child = client.post(
        "/api/v1/children",
        headers=headers,
        json={"nickname": "큰이", "gender": "MALE", "birthYearMonth": "2019-01"},
    )
    child_id = child.json()["data"]["id"]
    invalid_age = client.post(
        f"/api/v1/children/{child_id}/measurements",
        headers=headers,
        json={"type": "SELF", "measuredAt": "2026-07-19", "items": [{"itemKey": "CARDIO", "value": 10}]},
    )
    assert invalid_age.status_code == 422
    duplicate_items = client.post(
        f"/api/v1/children/{child_id}/measurements",
        headers=headers,
        json={
            "type": "SELF",
            "measuredAt": "2022-01-19",
            "items": [{"itemKey": "CARDIO", "value": 10}, {"itemKey": "CARDIO", "value": 11}],
        },
    )
    assert duplicate_items.status_code == 422


def test_centers_activities_and_regional_insights(client: TestClient):
    headers = auth_headers(client, "content@example.com")
    db = SessionLocal()
    db.add_all(
        [
            Center(ext_center_id="center-1", name="강남 센터", address="서울 강남구 테헤란로 1", sido_sigungu="서울 강남구", latitude=37.5, longitude=127.0, measure_count=10),
            Center(ext_center_id="center-2", name="부산 센터", address="부산 해운대구 센텀로 1", sido_sigungu="부산 해운대구", latitude=35.1, longitude=129.1, measure_count=2),
        ]
    )
    db.add(ActivityVideo(ext_video_id="video-1", title="심폐 운동", fitness_element="CARDIO", age_group="PRESCHOOL", url="https://example.com/video"))
    db.commit()
    db.close()

    centers = client.get("/api/v1/centers?sidoSigungu=%EC%84%9C%EC%9A%B8%20%EA%B0%95%EB%82%A8%EA%B5%AC&lat=37.5&lng=127.0", headers=headers)
    assert centers.status_code == 200
    assert centers.json()["data"]["items"][0]["name"] == "강남 센터"
    assert centers.json()["data"]["items"][0]["distanceKm"] == 0

    name_search = client.get("/api/v1/centers?name=%EA%B0%95%EB%82%A8", headers=headers)
    assert name_search.status_code == 200
    assert [item["name"] for item in name_search.json()["data"]["items"]] == ["강남 센터"]

    address_search = client.get("/api/v1/centers?name=%EC%84%9C%EC%9A%B8", headers=headers)
    assert address_search.status_code == 200
    assert [item["name"] for item in address_search.json()["data"]["items"]] == ["강남 센터"]

    activities = client.get("/api/v1/activities?fitnessElement=CARDIO&ageGroup=PRESCHOOL", headers=headers)
    assert activities.status_code == 200
    assert activities.json()["data"]["items"][0]["fitnessElement"] == "CARDIO"

    insight = client.get("/api/v1/insights/regional?sidoSigungu=%EC%84%9C%EC%9A%B8%20%EA%B0%95%EB%82%A8%EA%B5%AC", headers=headers)
    assert insight.status_code == 200
    assert insight.json()["data"]["regionMeasureCount"] == 10

    region_map = client.get("/api/v1/insights/regional/map", headers=headers)
    assert region_map.status_code == 200
    assert region_map.json()["data"]["fallback"] is False


def test_admin_sync_upserts_external_cache(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    settings = get_settings()
    original = (settings.kspo_api_key, settings.kspo_center_url, settings.kspo_activity_url)
    settings.kspo_api_key = "test-key"
    settings.kspo_center_url = "https://example.com/centers"
    settings.kspo_activity_url = "https://example.com/activities"

    class FakeKspoClient:
        def __init__(self, api_key: str):
            assert api_key == "test-key"

        def fetch_centers(self, url: str, page_size: int = 100) -> list[CenterRecord]:
            assert url.endswith("centers")
            return [
                CenterRecord(
                    "sync-center",
                    "동기화 센터",
                    "서울 중구 세종대로 1",
                    "서울 중구",
                    37.56,
                    126.97,
                    sido="서울특별시",
                )
            ]

        def fetch_activities(self, url: str, page_size: int = 100) -> list[ActivityRecord]:
            assert url.endswith("activities")
            return [ActivityRecord("sync-video", "동기화 운동", "CARDIO", "PRESCHOOL", "https://example.com/sync")]

    monkeypatch.setattr("app.api.v1.internal.KspoClient", FakeKspoClient)
    db = SessionLocal()
    admin = Parent(email="admin@example.com", password_hash="unused", is_admin=True)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    token = create_access_token(admin.id, True)
    db.close()

    try:
        response = client.post(
            "/api/v1/internal/sync",
            headers={"Authorization": f"Bearer {token}"},
            json={"targets": ["CENTERS", "ACTIVITIES"]},
        )
        assert response.status_code == 200
        assert response.json()["data"]["synced"] == {"centers": 1, "activities": 1}
        db = SessionLocal()
        center = db.query(Center).filter_by(ext_center_id="sync-center").one()
        assert center.sido == "서울특별시"
        assert db.query(ActivityVideo).filter_by(ext_video_id="sync-video").count() == 1
        db.close()
    finally:
        settings.kspo_api_key, settings.kspo_center_url, settings.kspo_activity_url = original


def test_cron_sync_rejects_invalid_secret(client: TestClient):
    settings = get_settings()
    original = settings.cron_secret
    settings.cron_secret = "cron-test-secret"
    try:
        response = client.get(
            "/api/v1/internal/cron-sync/centers",
            headers={"Authorization": "Bearer wrong-secret"},
        )
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "AUTH_UNAUTHORIZED"
    finally:
        settings.cron_secret = original


def test_admin_activity_page_sync_commits_one_page(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    settings = get_settings()
    original = (settings.kspo_api_key, settings.kspo_activity_url)
    settings.kspo_api_key = "test-key"
    settings.kspo_activity_url = "https://example.com/activities"

    class FakeKspoClient:
        def __init__(self, api_key: str):
            assert api_key == "test-key"

        def fetch_activities_page(self, url: str, page_no: int, page_size: int):
            assert url.endswith("activities")
            assert page_no == 2
            assert page_size == 100
            return [ActivityRecord("page-video", "페이지 운동", "CARDIO", "PRESCHOOL", "https://example.com/page")], 201

    monkeypatch.setattr("app.api.v1.internal.KspoClient", FakeKspoClient)
    db = SessionLocal()
    admin = Parent(email="page-admin@example.com", password_hash="unused", is_admin=True)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    token = create_access_token(admin.id, True)
    db.close()

    try:
        response = client.post(
            "/api/v1/internal/sync?page=2&page_size=100",
            headers={"Authorization": f"Bearer {token}"},
            json={"targets": ["ACTIVITIES"]},
        )
        assert response.status_code == 200
        assert response.json()["data"]["page"] == 2
        assert response.json()["data"]["totalPages"] == 3
        assert response.json()["data"]["hasNext"] is True
        db = SessionLocal()
        assert db.query(ActivityVideo).filter_by(ext_video_id="page-video").count() == 1
        db.close()
    finally:
        settings.kspo_api_key, settings.kspo_activity_url = original


def test_cron_sync_runs_target_with_secret(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    settings = get_settings()
    original = (settings.cron_secret, settings.kspo_api_key, settings.kspo_center_url)
    settings.cron_secret = "cron-test-secret"
    settings.kspo_api_key = "test-key"
    settings.kspo_center_url = "https://example.com/centers"

    class FakeKspoClient:
        def __init__(self, api_key: str):
            assert api_key == "test-key"

        def fetch_centers(self, url: str, page_size: int = 100) -> list[CenterRecord]:
            assert url.endswith("centers")
            return [CenterRecord("cron-center", "Cron 센터", "서울 중구 세종대로 1", "서울 중구", None, None, 7)]

        def fetch_activities(self, url: str, page_size: int = 100) -> list[ActivityRecord]:
            raise AssertionError(f"unexpected activity sync: {url}")

    monkeypatch.setattr("app.api.v1.internal.KspoClient", FakeKspoClient)
    try:
        response = client.get(
            "/api/v1/internal/cron-sync/centers",
            headers={"Authorization": "Bearer cron-test-secret"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["targets"] == ["CENTERS"]
        assert response.json()["data"]["synced"] == {"centers": 1, "activities": 0}
    finally:
        settings.cron_secret, settings.kspo_api_key, settings.kspo_center_url = original
