from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount_less_than_invested,
    check_name_duplicate,
    check_project_already_closed,
    check_project_exists,
    check_project_has_investments
)
from app.core.db import get_async_session
from app.crud.base import CRUDBase
from app.models import CharityProject, Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)


router = APIRouter()
charity_project_crud = CRUDBase(CharityProject)
donation_crud = CRUDBase(Donation)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Показывает все проекты."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание проекта."""
    await check_name_duplicate(project_in.name, session)

    return await charity_project_crud.create(
        obj_in=project_in,
        opposing_crud=donation_crud,
        session=session
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Изменение проекта."""
    db_project = await check_project_exists(project_id, session)

    check_project_already_closed(db_project)

    if project_in.name is not None:
        await check_name_duplicate(project_in.name, session)

    if project_in.full_amount is not None:
        check_full_amount_less_than_invested(
            db_project, project_in.full_amount
        )

    return await charity_project_crud.update(
        db_obj=db_project,
        obj_in=project_in,
        session=session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить целевой проект."""
    db_project = await check_project_exists(project_id, session)
    check_project_already_closed(db_project)
    check_project_has_investments(db_project)

    return await charity_project_crud.remove(
        db_obj=db_project, session=session
    )
