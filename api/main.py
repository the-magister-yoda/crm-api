from fastapi import FastAPI, HTTPException
from database import Database
from api.schemas import CustomerCreate, ProductCreate, CustomerResponse, CustomerUpdate, ProductResponse
from models import Customer, Goods
from typing import List


app = FastAPI()
db = Database()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/customers")
def create_customer(customer: CustomerCreate):
    new_customer = Customer(
        name=customer.name,
        phone=customer.phone
    )
    db.add_customer(new_customer)
    return {"status": "created"}


@app.get("/customers", response_model=List[CustomerResponse])
def show_customers():    
    return db.show_customers()


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def show_customer(customer_id: int):
    try:
        customer = db.get_customer(customer_id)
        return customer
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )


@app.patch("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer_data: CustomerUpdate):
    try:
        name = customer_data.name
        phone = customer_data.phone
        customer = db.update_customer(customer_id, name, phone)
        return customer
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=''
        )

@app.delete("/customers/{customer_id}", response_model=CustomerResponse)
def delete_customer(customer_id: int):
    try:
        customer = db.delete_customer(customer_id)
        return customer
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail='Customer not found, or already deleted'
        )



@app.get("/products", response_model=List[ProductResponse])
def show_products():
    return db.show_products()


@app.post("/products")
def create_product(product: ProductCreate):
    new_product = Goods(
        name=product.name,
        price=product.price,
        quantity=product.quantity
    )
    db.add_product(new_product)
    return {"status": "created"}


