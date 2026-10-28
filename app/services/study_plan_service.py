
from datetime import date

from app.models.study_plan import StudyPlan
from app.repositories.study_plan_repository import StudyPlanRepository
from app.schemas.study_plan import StudyPlanCreate, StudyPlanUpdate


class StudyPlanService:
    """Menangani logika bisnis target belajar."""

    def __init__(self, repository: StudyPlanRepository):
        self.repository = repository

    def get_all(self) -> list[StudyPlan]:
        return self.repository.get_all()

    def get_by_id(self, plan_id: int) -> StudyPlan:
        plan = self.repository.get_by_id(plan_id)

        if plan is None:
            raise ValueError("Target belajar tidak ditemukan")

        return plan

    def create(self, data: StudyPlanCreate) -> StudyPlan:
        if data.deadline < date.today():
            raise ValueError("Deadline tidak boleh di masa lalu")

        plan = StudyPlan(
            id=0,
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            priority=data.priority,
        )

        return self.repository.add(plan)

    def update(self, plan_id: int, data: StudyPlanUpdate) -> StudyPlan:
        existing = self.get_by_id(plan_id)

        if data.deadline < date.today():
            raise ValueError("Deadline tidak boleh di masa lalu")

        updated = StudyPlan(
            id=existing.id,
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            priority=data.priority,
            status=existing.status,
        )

        return self.repository.update(updated)

    def update_status(self, plan_id: int, status: str) -> StudyPlan:
        existing = self.get_by_id(plan_id)

        updated = StudyPlan(
            id=existing.id,
            title=existing.title,
            description=existing.description,
            deadline=existing.deadline,
            priority=existing.priority,
            status=status,
        )

        return self.repository.update(updated)

    def delete(self, plan_id: int) -> None:
        self.get_by_id(plan_id)
        self.repository.delete(plan_id)