from dataclasses import dataclass
from datetime import date
from typing import Literal


@dataclass
class StudyPlan:
    id: int
    title: str
    description: str
    deadline: date
    priority: Literal["low", "medium", "high"]
    status: Literal["pending", "in_progress", "completed"] = "pending"