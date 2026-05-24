from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def close_donation_or_project(obj) -> None:
    """Вспомогательная функция для закрытия объекта."""
    obj.fully_invested = True
    obj.close_date = datetime.now(timezone.utc)


async def invest_money(
    session: AsyncSession,
) -> None:
    """Универсальная функция распределения свободных денег по проектам."""
    projects_query = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested.is_(False))
        .order_by(CharityProject.create_date)
    )
    open_projects = projects_query.scalars().all()

    donations_query = await session.execute(
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(Donation.create_date)
    )
    open_donations = donations_query.scalars().all()

    if not open_projects or not open_donations:
        return

    for project in open_projects:
        for donation in open_donations:
            if donation.fully_invested:
                continue

            project_needed = project.full_amount - project.invested_amount
            donation_available = (
                donation.full_amount - donation.invested_amount
            )

            money_to_invest = min(project_needed, donation_available)

            project.invested_amount += money_to_invest
            donation.invested_amount += money_to_invest

            if donation.invested_amount == donation.full_amount:
                close_donation_or_project(donation)

            if project.invested_amount == project.full_amount:
                close_donation_or_project(project)
                break

        session.add(project)

        for donation in open_donations:
            session.add(donation)
