from typing import Optional
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    status: str

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
