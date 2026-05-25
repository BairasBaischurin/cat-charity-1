from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_async_session
from app.models import CharityProject, Donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB
)
from app.services.investing import create_and_invest


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Вывод списка всех пожертвований."""
    result = await session.execute(
        select(Donation).order_by(Donation.create_date)
    )
    return result.scalars().all()


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
    return await create_and_invest(
        donation_in, Donation, CharityProject, session
    )
