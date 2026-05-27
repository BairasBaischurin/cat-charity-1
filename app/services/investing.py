from app.models.base import InvestmentModel


def invest_money(
    target: InvestmentModel,
    sources: list[InvestmentModel],
) -> list[InvestmentModel]:
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
