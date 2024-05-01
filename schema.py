from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
from decimal import Decimal


class ChainBase(BaseModel):
    chain_id: int
    name: str
    native_token: str
    wrapped_token_address: str
    dbank_id: str


class Chain(ChainBase):
    id: int


class TokenBase(BaseModel):
    name: str
    symbol: str
    address: str
    decimals: int
    chain_id: int
    usd_value: Optional[Decimal] = None
    usd_check: datetime

    @field_validator("usd_value")
    def validate_usd_value(cls, v):
        if v is None:
            return Decimal(0)
        return v


class Token(TokenBase):
    id: int
