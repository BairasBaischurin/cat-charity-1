from app.models.base import Base


def invest_money(
    target: Base,
    sources: list[Base],
) -> list[Base]:
    """Функция распределения средств."""
    changed = []

    for source in sources:
        if target.fully_invested:
            break

        changed.append(source)

        money_to_invest = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )

        if money_to_invest == 0:
            changed.pop()
            continue

        for obj in (target, source):
            obj.invested_amount += money_to_invest
            obj.close()

    return changed
