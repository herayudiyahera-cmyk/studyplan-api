
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.sqlite_study_plan_repository import (
    SQLiteStudyPlanRepository,
)
from app.schemas.study_plan import (
    StudyPlanCreate,
    StudyPlanResponse,
    StudyPlanStatusUpdate,
    StudyPlanUpdate,
)
from app.services.study_plan_service import StudyPlanService


router = APIRouter(prefix="/api/v1/study-plans", tags=["Study Plans"])

_repository = SQLiteStudyPlanRepository()


def get_service() -> StudyPlanService:
    return StudyPlanService(_repository)


ServiceDependency = Annotated[StudyPlanService, Depends(get_service)]


@router.post(
    "",
    response_model=StudyPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_study_plan(
    data: StudyPlanCreate,
    service: ServiceDependency,
):
    try:
        return service.create(data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("", response_model=list[StudyPlanResponse])
def get_study_plans(service: ServiceDependency):
    return service.get_all()


@router.get("/{plan_id}", response_model=StudyPlanResponse)
def get_study_plan(plan_id: int, service: ServiceDependency):
    try:
        return service.get_by_id(plan_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{plan_id}", response_model=StudyPlanResponse)
def update_study_plan(
    plan_id: int,
    data: StudyPlanUpdate,
    service: ServiceDependency,
):
    try:
        return service.update(plan_id, data)
    except ValueError as error:
        code = 400 if "Deadline" in str(error) else 404
        raise HTTPException(status_code=code, detail=str(error))


@router.patch("/{plan_id}/status", response_model=StudyPlanResponse)
def update_study_plan_status(
    plan_id: int,
    data: StudyPlanStatusUpdate,
    service: ServiceDependency,
):
    try:
        return service.update_status(plan_id, data.status)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study_plan(plan_id: int, service: ServiceDependency):
    try:
        service.delete(plan_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
