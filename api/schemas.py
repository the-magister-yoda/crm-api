from typing import Optional
from pydantic import BaseModel
from datetime import datetime


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

class OrderCreate(BaseModel):
    customer_id: int
    
class OrderResponse(BaseModel):
    id: int
    customer_id: int
    created_at: datetime
    status: str

class AddOrderItem(BaseModel):
    goods_id: int
    quantity: int

class ShowOrderDetails(BaseModel):
    name: str
    quantity: int
    price: float
    total: float
  




