from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .domain import FinPayDomain
from .models import TransferRequest


app = FastAPI(
    title="FinPay Sandbox API",
    description="Training fintech API for QA course.",
    version="0.1.0",
)

domain = FinPayDomain()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/test/reset")
def reset_state():
    domain.reset()
    return {"status": "reset"}


@app.get("/accounts/{account_id}")
def get_account(account_id: str):
    account = domain.get_account(account_id)
    if not account:
        raise HTTPException(
            status_code=404,
            detail={"code": "ACCOUNT_NOT_FOUND", "message": "Account not found"},
        )
    return JSONResponse(content=jsonable_encoder(account))


@app.post("/transfer")
def create_transfer(request: TransferRequest):
    try:
        result = domain.transfer(
            from_account=request.from_account,
            to_account=request.to_account,
            amount=request.amount,
            idempotency_key=request.idempotency_key,
        )
        return JSONResponse(content=jsonable_encoder(result))
    except ValueError as exc:
        code = str(exc)
        status_map = {
            "ACCOUNT_NOT_FOUND": 404,
            "CURRENCY_MISMATCH": 409,
            "INVALID_AMOUNT": 422,
            "INSUFFICIENT_FUNDS": 409,
        }
        raise HTTPException(
            status_code=status_map.get(code, 400),
            detail={"code": code, "message": code.replace("_", " ").title()},
        )
