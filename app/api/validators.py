from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверяет уникальность имени проекта."""
    db_project_id = await session.execute(
        select(CharityProject.id).where(CharityProject.name == project_name)
    )
    db_project_id = db_project_id.scalars().first()

    if db_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Проект с именем "{project_name}" уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверяет существование проекта по ID и возвращает его."""
    db_project = await session.get(CharityProject, project_id)

    if db_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!',
        )
    return db_project


def check_project_already_closed(
    project: CharityProject,
) -> None:
    """Запрещает редактирование или удаление закрытого проекта."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


def check_full_amount_less_than_invested(
    project: CharityProject,
    new_full_amount: int,
) -> None:
    """Запрещает устанавливать требуемую сумму меньше уже внесенной."""
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Нелья установить значение {new_full_amount} если'
            f'сумма внесенной равна {project.invested_amount}',
        )


def check_project_has_investments(
    project: CharityProject,
) -> None:
    """Запрещает удалять проект, если в него уже поступили пожертвования."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект уже внесены средства, его нельзя удалить!',
        )
