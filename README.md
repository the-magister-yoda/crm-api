# CRM API (Flowers Shop)

REST API for managing customers, products, and orders.
The project is created for real production systems.

For a Russian-speaking audience:

(REST API для управления клиентами, товарами и заказами. Это crm система для цветочного магазина сюда я не стал выкладывать весь функционал так как считаю это не нужным и будет не честным по отношению к заказчику, оставил только самое минимальное но в принципе этого и хватает. Для ознакомление листайте вниз здесь есть вся необходимая информация.)

## Tech Stack
- Python 3.10+
- FastAPI
- SQLite
- Pydantic
- Uvicorn

## Project Setup

Clone the repository:

git clone https://github.com/the-magister-yoda/crm.git

cd crm
Install dependencies:

pip install fastapi
Run the server: uvicorn api.main:app --reload

The API will be available at: http://127.0.0.1:8000

Swagger documentation: http://127.0.0.1:8000/docs


👤 Customers
Create customer
POST /customers

{
  "name": "Daniayr",
  "phone": "any number that you have"
}

Get customers: GET /customers


All customers (including inactive): GET /customers?search=all

Get customer by ID: GET /customers/{customer_id}

Update customer: PATCH /customers/{customer_id}

{
  "name": "New name",
  "phone": "new phone number"
}

Delete customer (soft delete)

DELETE /customers/{customer_id}

📦 Products
Create product
POST /products

{
  "name": "Rose",
  "price": 10.5,
  "quantity": 100
}

Get all products

GET /products


🧾 Orders
Create order

POST /orders
{
  "customer_id": 1
}

Add product to order
POST /orders/{order_id}/items

{
  "goods_id": 1,
  "quantity": 3
}


Get order details
GET /orders/{order_id}

Confirm order
PATCH /orders/{order_id}/confirm

Cancel order
PATCH /orders/{order_id}/cancel


Business Rules

You cannot:

create an order for a non-existent or inactive customer

add items to an order that is not in created status

cancel a paid order

Product stock decreases when items are added to an order

Product stock is restored when an order is canceled




Statuses:

Customer: active, inactive

Order: created, confirmed, paid, canceled

