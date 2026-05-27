from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import InvestmentModel


class CRUDBase:
<<<<<<< HEAD
    def __init__(self, model: type[InvestmentModel]):
=======
    def __init__(self, model: type[Base]):
>>>>>>> c5ba1e07413c7d51442824b51dabc5f158de6a40
        self.model = model

    async def get_multi(self, session: AsyncSession, order_by_field=None):
        """Показывает все объекты."""
        query = select(self.model)
        if order_by_field is not None:
            query = query.order_by(order_by_field)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ):
        """Получить ID объекта по его имени."""
        db_project_id = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return db_project_id.scalars().first()

<<<<<<< HEAD
    async def create(self, obj_in, session: AsyncSession):
=======
    async def create(self, obj_in, opposing_crud, session: AsyncSession):
>>>>>>> c5ba1e07413c7d51442824b51dabc5f158de6a40
        """Создать запись."""
        new_object = self.model(**obj_in.model_dump())
        session.add(new_object)
        await session.flush()
<<<<<<< HEAD
=======

        uninvested_sources = await opposing_crud.get_uninvested(session)
        updated_sources = invest_money(
            target=new_object, sources=uninvested_sources
        )
        session.add_all(updated_sources)
        await session.commit()
        await session.refresh(new_object)
>>>>>>> c5ba1e07413c7d51442824b51dabc5f158de6a40
        return new_object

    async def get_uninvested(self, session: AsyncSession):
        """Извлечь незавершенные объекты."""
        query = (
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def update(self, db_obj, obj_in, session: AsyncSession):
        """Обновляет объекты."""
        update_data = obj_in.model_dump(exclude_unset=True)
<<<<<<< HEAD
        for field, value in update_data.items():
            setattr(db_obj, field, value)
=======

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        if hasattr(db_obj, 'closing_fully_invested_project'):
            db_obj.closing_fully_invested_project()

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
>>>>>>> c5ba1e07413c7d51442824b51dabc5f158de6a40
        return db_obj

    async def remove(self, db_obj, session: AsyncSession):
        """Удаляет проекты."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
