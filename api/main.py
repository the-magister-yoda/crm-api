from fastapi import FastAPI
from database import Database
from api.schemas import CustomerCreate, ProductCreate
from models import Customer, Goods


app = FastAPI()
db = Database()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/customers")
def show_customers():
    customers = db.show_customers()
    result = []
    for customer in customers:
        result.append({
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone
        })
    return result


@app.post("/customers")
def create_customer(customer: CustomerCreate):
    new_customer = Customer(
        name=customer.name,
        phone=customer.phone
    )
    db.add_customer(new_customer)
    return {"status": "created"}


@app.get("/products")
def show_products():
    products = db.show_products()
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        })
    return result


@app.post("/products")
def create_product(product: ProductCreate):
    new_product = Goods(
        name=product.name,
        price=product.price,
        quantity=product.quantity
    )
    db.add_product(new_product)
    return {"status": "created"}


