from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_async_session
from app.models import Donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB
)
from app.services.investing import invest_money


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationFullInfoDB],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Вывод списка всех пожертвований."""
    result = await session.execute(
        select(Donation).order_by(Donation.create_date)
    )
    all_donations = result.scalars().all()
    return all_donations


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
    new_donation = Donation(**donation_in.model_dump())

    session.add(new_donation)
    await session.flush()

    await invest_money(session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
