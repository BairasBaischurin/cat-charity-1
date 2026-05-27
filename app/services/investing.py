from app.models.base import Base


def invest_money(
    target: Base,
    sources: list[Base],
) -> list[Base]:
    """Функция распределения средств."""
    changed = []

    for source in sources:
        changed.append(source)

        money_to_invest = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )

        for obj in (target, source):
            obj.invested_amount += money_to_invest
            obj.closing_fully_invested_project()

        if target.fully_invested:
            break

    return changed
