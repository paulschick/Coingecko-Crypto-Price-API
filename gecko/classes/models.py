from pydantic import BaseModel
from typing import List


class SimplePriceResponse(BaseModel):
    id: str
    quote: str
    price: float


class CoinsResponse(BaseModel):
    id: str
    symbol: str
    name: str


class CurrencyDetails(BaseModel):
    id: str
    symbol: str
    price: str = ''


class PriceCollection(BaseModel):
    timestamp: str = ""
    prices: List[CurrencyDetails] = []
    unsupported: List[str] = []
