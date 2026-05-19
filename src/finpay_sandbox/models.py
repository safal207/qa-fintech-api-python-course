from decimal import Decimal
from pydantic import BaseModel, Field


class Account(BaseModel):
    id: str
    currency: str = "USD"
    balance: Decimal = Field(decimal_places=2)


class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: Decimal = Field(decimal_places=2)
    idempotency_key: str


class TransferResponse(BaseModel):
    transfer_id: str
    status: str
    from_account: str
    to_account: str
    amount: Decimal
    fee: Decimal
    idempotency_key: str


class ErrorResponse(BaseModel):
    code: str
    message: str
