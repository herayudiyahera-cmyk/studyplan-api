
from datetime import date, timedelta

from app.models.study_plan import StudyPlan
from app.repositories.sqlite_study_plan_repository import (
    SQLiteStudyPlanRepository,
)


def create_sample_plan():
    return StudyPlan(
        id=0,
        title="Belajar SQLite",
        description="Menguji penyimpanan database",
        deadline=date.today() + timedelta(days=7),
        priority="high",
        status="pending",
    )


def test_save_and_get_plan(tmp_path):
    db_path = tmp_path / "test_studyplan.db"
    repository = SQLiteStudyPlanRepository(str(db_path))

    saved = repository.add(create_sample_plan())
    result = repository.get_by_id(saved.id)

    assert saved.id == 1
    assert result is not None
    assert result.title == "Belajar SQLite"
    assert result.priority == "high"


def test_data_persists_after_reopening_database(tmp_path):
    db_path = tmp_path / "persistent.db"

    repository1 = SQLiteStudyPlanRepository(str(db_path))
    saved = repository1.add(create_sample_plan())

    # Membuka repository baru menggunakan file database yang sama
    repository2 = SQLiteStudyPlanRepository(str(db_path))
    result = repository2.get_by_id(saved.id)

    assert result is not None
    assert result.title == "Belajar SQLite"


def test_update_plan(tmp_path):
    db_path = tmp_path / "update.db"
    repository = SQLiteStudyPlanRepository(str(db_path))

    plan = repository.add(create_sample_plan())
    plan.status = "completed"

    repository.update(plan)
    result = repository.get_by_id(plan.id)

    assert result is not None
    assert result.status == "completed"


def test_delete_plan(tmp_path):
    db_path = tmp_path / "delete.db"
    repository = SQLiteStudyPlanRepository(str(db_path))

    plan = repository.add(create_sample_plan())

    assert repository.delete(plan.id) is True
    assert repository.get_by_id(plan.id) is None
