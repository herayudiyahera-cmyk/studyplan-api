
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.study_plan_repository import (
    InMemoryStudyPlanRepository,
)
from app.routers.study_plan_router import get_service
from app.services.study_plan_service import StudyPlanService


# Satu repository yang digunakan selama setiap pengujian
test_repository = InMemoryStudyPlanRepository()


def override_get_service():
    return StudyPlanService(test_repository)


app.dependency_overrides[get_service] = override_get_service
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_repository():
    test_repository._plans.clear()
    test_repository._next_id = 1
    yield


def test_create_study_plan_api():
    response = client.post(
        "/api/v1/study-plans",
        json={
            "title": "Belajar FastAPI",
            "description": "Menguji endpoint API",
            "deadline": str(date.today() + timedelta(days=7)),
            "priority": "high",
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Belajar FastAPI"


def test_get_study_plans_api():
    client.post(
        "/api/v1/study-plans",
        json={
            "title": "Belajar Python",
            "description": "Latihan backend",
            "deadline": str(date.today() + timedelta(days=7)),
            "priority": "medium",
        },
    )

    response = client.get("/api/v1/study-plans")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Belajar Python"


def test_get_missing_study_plan_api():
    response = client.get("/api/v1/study-plans/999")

    assert response.status_code == 404


def test_reject_invalid_study_plan_api():
    response = client.post(
        "/api/v1/study-plans",
        json={
            "title": "AB",
            "description": "Judul terlalu pendek",
            "deadline": str(date.today() + timedelta(days=7)),
            "priority": "high",
        },
    )

    assert response.status_code == 422
