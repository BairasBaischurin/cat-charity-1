from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base


async def create_and_invest(
    model_in,
    model_cls: type[Base],
    opposing_model_cls: type[Base],
    session: AsyncSession
) -> Base:
    """Создает объект и запускает процесс инвестирования."""
    new_object = model_cls(**model_in.model_dump())
    session.add(new_object)
    await session.flush()

    query = (
        select(opposing_model_cls)
        .where(opposing_model_cls.fully_invested.is_(False))
        .order_by(opposing_model_cls.create_date)
    )
    result = await session.execute(query)
    uninvested_projects = list(result.scalars().all())

    updated_projects = invest_money(
        target=new_object, sources=uninvested_projects
    )

    if updated_projects:
        session.add_all(updated_projects)

    await session.commit()
    await session.refresh(new_object)
    return new_object


def invest_money(
    target: Base,
    sources: list[Base],
) -> list[Base]:
    """Функция распределения средств."""
    changed_objects = []

    for source in sources:
        target_needed = target.full_amount - target.invested_amount
        if target_needed == 0:
            break

        source_available = source.full_amount - source.invested_amount
        if source_available == 0:
            continue

        money_to_invest = min(target_needed, source_available)

        target.invested_amount += money_to_invest
        source.invested_amount += money_to_invest

        changed_objects.append(source)

        if source.invested_amount == source.full_amount:
            source.close()

        if target.invested_amount == target.full_amount:
            target.close()
            break

    return changed_objects
