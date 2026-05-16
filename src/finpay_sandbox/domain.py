from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4


FEE_RATE = Decimal("0.01")


class FinPayDomain:
    def __init__(self):
        self.accounts = {
            "acc_alex": {"id": "acc_alex", "currency": "USD", "balance": Decimal("1000.00")},
            "acc_yura": {"id": "acc_yura", "currency": "USD", "balance": Decimal("100.00")},
        }
        self.idempotency_store = {}

    def reset(self):
        self.__init__()

    def get_account(self, account_id: str):
        return self.accounts.get(account_id)

    def calculate_fee(self, amount: Decimal) -> Decimal:
        return (amount * FEE_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def transfer(self, from_account: str, to_account: str, amount: Decimal, idempotency_key: str):
        if idempotency_key in self.idempotency_store:
            return self.idempotency_store[idempotency_key]

        source = self.accounts.get(from_account)
        target = self.accounts.get(to_account)

        if source is None or target is None:
            raise ValueError("ACCOUNT_NOT_FOUND")

        if source["currency"] != target["currency"]:
            raise ValueError("CURRENCY_MISMATCH")

        if amount <= 0:
            raise ValueError("INVALID_AMOUNT")

        fee = self.calculate_fee(amount)
        total = amount + fee

        if source["balance"] < total:
            raise ValueError("INSUFFICIENT_FUNDS")

        source["balance"] -= total
        target["balance"] += amount

        result = {
            "transfer_id": f"tr_{uuid4().hex[:12]}",
            "status": "completed",
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "fee": fee,
            "idempotency_key": idempotency_key,
        }
        self.idempotency_store[idempotency_key] = result
        return result
