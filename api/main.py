from fastapi import FastAPI, HTTPException
from database import Database
from api.schemas import CustomerCreate, ProductCreate, CustomerResponse, CustomerUpdate, ProductResponse, OrderResponse, OrderCreate, AddOrderItem, ShowOrderDetails
from errors import CustomerEmpty, CustomerNotFound, CustomerInactive, NotEnoughQuantity, OrderNotFound, ProductNotFound, OrderInactive, OrderAlreadyPaid, PhoneNumberIsTaken, OrderPacked, OrderEmpty
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
    try:
        db.add_customer(new_customer)
        return {"status": "created"}

    except PhoneNumberIsTaken:
        raise HTTPException(
            status_code=409,
            detail='This phone number is already taken'
        )


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


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    try:
        customer = db.delete_customer(customer_id)
        return {"status": "deleted successfully"}
    
    except CustomerNotFound:
        raise HTTPException(
            status_code=404,
            detail='Customer not found'
        )

    except CustomerInactive:
        raise HTTPException(
            status_code=409,
            detail='Customer is already inactive'
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


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        db.delete_prodcut(product_id)
        return {"status": "successfully"}

    except ProductNotFound:
        raise HTTPException(
            status_code=404,
            detail='Product not found'
        )


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

    except OrderPacked:
        raise HTTPException(
            status_code=400,
            detail='Order is already created and packed'
        )


@app.post("/orders/{order_id}/items")
def add_products_to_order(order_id: int, item: AddOrderItem):
    try:
        db.add_order_details(
            order_id=order_id,
            goods_id=item.goods_id,
            quantity=item.quantity
        )
        return {"status": "item added"}
    
    except OrderNotFound:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    except OrderAlreadyPaid:
        raise HTTPException(
            status_code=400,
            detail='Order is already paid you can not add products to order anymore'
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
    

@app.patch("/orders/{order_id}/cancel")
def cancel_order(order_id: int):
    try:
        db.cancel_order(order_id)
        return {"status": "canceled"}

    except OrderNotFound:
        raise HTTPException(
            status_code=404,
            detail='Order not found'
        )
    
    except OrderAlreadyPaid:
        raise HTTPException(
            status_code=400,
            detail='Order already paid it can not be canceled'
        )
    
    except ProductNotFound:
        raise HTTPException(
            status_code=400,
            detail='There are no items in order'
        )
    

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    try:
        db.confirm_order(order_id)
        return {"status": "confirmed"}
    
    except OrderNotFound:
        raise HTTPException(
            status_code=404,
            detail='Order not found'
        )
    
    except ProductNotFound:
        raise HTTPException(
            status_code=400,
            detail='There are no goods in order'
        )
    
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Order cannot be confirmed'
        )


@app.post("/orders/{order_id}/pay")
def pay_for_order(order_id: int):
    try:
        db.pay_for_order(order_id=order_id)
        return {"status": "Order has been paid"}

    except OrderNotFound:
        raise HTTPException(
            status_code=404,
            detail='Order not found'
        )

    except OrderAlreadyPaid:
        raise HTTPException(
            status_code=400,
            detail='Order is already paid'
        )

    except OrderInactive:
        raise HTTPException(
            status_code=400,
            detail='Order is not active it can not proceed payment'
        )

    except OrderEmpty:
        raise HTTPException(
            status_code=400,
            detail='Order is empty'
        )

