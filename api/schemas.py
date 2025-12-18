from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone: str


class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
