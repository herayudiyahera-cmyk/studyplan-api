
from datetime import date, timedelta

import pytest

from app.repositories.study_plan_repository import (
    InMemoryStudyPlanRepository,
)
from app.schemas.study_plan import StudyPlanCreate, StudyPlanUpdate
from app.services.study_plan_service import StudyPlanService


@pytest.fixture
def service():
    repository = InMemoryStudyPlanRepository()
    return StudyPlanService(repository)


def test_create_study_plan(service):
    data = StudyPlanCreate(
        title="Belajar Python",
        description="Belajar dasar Python",
        deadline=date.today() + timedelta(days=7),
        priority="high",
    )

    result = service.create(data)

    assert result.id == 1
    assert result.title == "Belajar Python"
    assert result.status == "pending"


def test_get_all_study_plans(service):
    data = StudyPlanCreate(
        title="Belajar FastAPI",
        description="Membuat backend",
        deadline=date.today() + timedelta(days=7),
        priority="medium",
    )

    service.create(data)

    results = service.get_all()

    assert len(results) == 1
    assert results[0].title == "Belajar FastAPI"


def test_update_study_plan_status(service):
    data = StudyPlanCreate(
        title="Belajar SQL",
        description="Latihan query",
        deadline=date.today() + timedelta(days=7),
        priority="low",
    )

    plan = service.create(data)
    updated = service.update_status(plan.id, "in_progress")

    assert updated.status == "in_progress"


def test_reject_past_deadline(service):
    data = StudyPlanCreate(
        title="Belajar Java",
        description="Latihan OOP",
        deadline=date.today() - timedelta(days=1),
        priority="high",
    )

    with pytest.raises(ValueError, match="Deadline"):
        service.create(data)


def test_plan_not_found(service):
    with pytest.raises(ValueError, match="tidak ditemukan"):
        service.get_by_id(999)
