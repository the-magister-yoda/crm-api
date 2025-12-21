from fastapi import FastAPI, HTTPException
from database import Database
from api.schemas import CustomerCreate, ProductCreate, CustomerResponse, CustomerUpdate, ProductResponse, OrderResponse, OrderCreate, AddOrderItem, ShowOrderDetails
from errors import CustomerEmpty, CustomerNotFound, CustomerInactive, NotEnoughQuantity, OrderNotFound, ProductNotFound, OrderInactive
from models import Customer, Goods, Order
from typing import List, Optional


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
def show_customers(search: Optional[str] = None):
    if search is None:
        customers = db.show_customers()
        res = []
        for customer in customers:
            if customer.status == 'active':
                res.append(customer)
        return res
    return db.show_customers()


# в общем так если мы что то передаем в search то он будет показывать всех покупателей
# и активных и не активных а если мы ничего не передаем то он будет показывать только активных клиентов
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
    
    except CustomerNotFound:
        raise HTTPException(
            status_code=404,
            detail='Customer not found'
        )
    
    except CustomerInactive:
        raise HTTPException(
            status_code=400,
            detail='Customer is inactive updates are not allowed'
        )
    
    except CustomerEmpty:
        raise HTTPException(
            status_code=400,
            detail='you must put any data for update'
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


@app.get("/orders", response_model=List[OrderResponse])
def show_orders():
    return db.show_orders()


@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate):
    new_order = Order(
        customer_id = order.customer_id
    )    

    try:
        order_id = db.create_order(new_order)
        new_order.id = order_id
        return new_order
    
    except CustomerNotFound:
        raise HTTPException(
            status_code=404,
            detail='Customer not found'
        )
    
    except CustomerInactive:
        raise HTTPException(
            status_code=400,
            detail='Oops Customer is inactive'
        )
    

@app.post("/orders/{order_id}/items")
def add_products_to_order(order_id: int, item: AddOrderItem):
    try:
        db.add_order_details(
            order_id = order_id,
            goods_id=item.goods_id,
            quantity=item.quantity
        )
        return {"status": "item added"}
    
    except OrderNotFound:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    
    except OrderInactive:
        raise HTTPException(
            status_code=400,
            detail='Order is inactive'
        )
    
    except ProductNotFound:
        raise HTTPException(
            status_code=404,
            detail='Product not found'
        )
    
    except NotEnoughQuantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough goods in stock"
        )
    
    
@app.get("/orders/{order_id}", response_model=List[ShowOrderDetails])
def show_order_details(order_id: int):
    try:
        return db.show_order_details(order_id)
    
    except OrderNotFound:
        raise HTTPException(
            status_code=404,
            detail='Order not found'
        )
    
    except OrderInactive:
        raise HTTPException(
            status_code=400,
            detail='Order were canceled'
        )
