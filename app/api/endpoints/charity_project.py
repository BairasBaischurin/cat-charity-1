from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_full_amount_less_than_invested,
    check_name_duplicate,
    check_project_already_closed,
    check_project_exists,
    check_project_has_investments
)
from app.core.db import get_async_session
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import invest_money


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Показывает все проекты."""
    result = await session.execute(select(CharityProject))
    all_projects = result.scalars().all()
    return all_projects


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
    new_project = CharityProject(**project_in.model_dump())

    session.add(new_project)
    await session.flush()

    await invest_money(session)
    await session.commit()
    await session.refresh(new_project)
    return new_project


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

    update_data = project_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_project, field, value)

    if db_project.full_amount == db_project.invested_amount:
        db_project.fully_invested = True
        db_project.close_date = datetime.now(timezone.utc)

    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)

    return db_project


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

    await session.delete(db_project)
    await session.commit()
    return db_project