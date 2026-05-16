from decimal import Decimal

from src.finpay_sandbox.domain import FinPayDomain


def test_fee_is_one_percent_rounded_to_cents():
    domain = FinPayDomain()

    assert domain.calculate_fee(Decimal('100.00')) == Decimal('1.00')
    assert domain.calculate_fee(Decimal('10.15')) == Decimal('0.10')
    assert domain.calculate_fee(Decimal('10.50')) == Decimal('0.11')
