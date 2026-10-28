from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class StudyPlanCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    deadline: date
    priority: Literal["low", "medium", "high"] = "medium"


class StudyPlanUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    deadline: date
    priority: Literal["low", "medium", "high"]


class StudyPlanStatusUpdate(BaseModel):
    status: Literal["pending", "in_progress", "completed"]


class StudyPlanResponse(BaseModel):
    id: int
    title: str
    description: str
    deadline: date
    priority: Literal["low", "medium", "high"]
    status: Literal["pending", "in_progress", "completed"]