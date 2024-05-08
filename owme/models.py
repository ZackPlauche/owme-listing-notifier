from pydantic import BaseModel
from decimal import Decimal


class Apartment(BaseModel):
    address: str
    number: int
    url: str
    price: Decimal | None = None
    available: bool