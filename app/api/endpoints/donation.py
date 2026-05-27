from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.base import CRUDBase
from app.models import CharityProject, Donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB
)
from app.services.investing import invest_money


router = APIRouter()
donation_crud = CRUDBase(Donation)
charity_project_crud = CRUDBase(CharityProject)


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Вывод списка всех пожертвований."""
    return await donation_crud.get_multi(
        session, order_by_field=Donation.create_date
    )


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создает пожертвование."""
    new_donation = await donation_crud.create(donation_in, session)
    uninvested_projects = await charity_project_crud.get_uninvested(session)
    updated_sources = invest_money(
        target=new_donation, sources=uninvested_projects
    )
    session.add_all(updated_sources)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
