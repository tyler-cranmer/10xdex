from pydantic import BaseModel
from datetime import datetime

class ChainBase(BaseModel):
    chain_id: int
    name: str
    native_token : str
    wrapped_token_address: str

class Chain(ChainBase):
    id: int

class TokenBase(BaseModel):
    name: str
    symbol: str 
    address: str
    decimals: int
    usd_value: float
    usd_check: datetime

class Token(TokenBase):
    id: int


    