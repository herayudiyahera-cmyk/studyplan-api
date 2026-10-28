
from abc import ABC, abstractmethod

from app.models.study_plan import StudyPlan


class StudyPlanRepository(ABC):
    """Kontrak untuk penyimpanan data target belajar."""

    @abstractmethod
    def get_all(self) -> list[StudyPlan]:
        pass

    @abstractmethod
    def get_by_id(self, plan_id: int) -> StudyPlan | None:
        pass

    @abstractmethod
    def add(self, plan: StudyPlan) -> StudyPlan:
        pass

    @abstractmethod
    def update(self, plan: StudyPlan) -> StudyPlan:
        pass

    @abstractmethod
    def delete(self, plan_id: int) -> bool:
        pass


class InMemoryStudyPlanRepository(StudyPlanRepository):
    """Implementasi repository menggunakan memori."""

    def __init__(self):
        self._plans: dict[int, StudyPlan] = {}
        self._next_id = 1

    def get_all(self) -> list[StudyPlan]:
        return list(self._plans.values())

    def get_by_id(self, plan_id: int) -> StudyPlan | None:
        return self._plans.get(plan_id)

    def add(self, plan: StudyPlan) -> StudyPlan:
        plan.id = self._next_id
        self._plans[self._next_id] = plan
        self._next_id += 1
        return plan

    def update(self, plan: StudyPlan) -> StudyPlan:
        self._plans[plan.id] = plan
        return plan

    def delete(self, plan_id: int) -> bool:
        return self._plans.pop(plan_id, None) is not None
