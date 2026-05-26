from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.services.investing import invest_money


async def create_and_invest(
    model_in,
    model_cls: type[Base],
    opposing_model_cls: type[Base],
    session: AsyncSession
) -> Base:
    """
    CRUD-метод: создает объект и запускает процесс инвестирования.
    """
    new_object = model_cls(**model_in.model_dump())
    session.add(new_object)
    await session.flush()

    query = (
        select(opposing_model_cls)
        .where(opposing_model_cls.fully_invested.is_(False))
        .order_by(opposing_model_cls.create_date)
    )
    result = await session.execute(query)
    uninvested_sources = list(result.scalars().all())

    updated_sources = invest_money(
        target=new_object, sources=uninvested_sources
    )

    if updated_sources:
        session.add_all(updated_sources)

    await session.commit()
    await session.refresh(new_object)
    return new_object
