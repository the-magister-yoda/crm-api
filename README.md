🌸 CRM API (Flower Shop)

REST API for managing customers, products, and orders in a flower shop.
The project demonstrates backend development skills, business logic implementation, and RESTful API design.

This repository contains the core functionality of a CRM system and is intended for demonstration and learning purposes.

🚀 Features

Customer management

Create, update, and soft-delete customers

Customer statuses: active, inactive

Product management

Create and list products

Stock quantity tracking

Order management

Create orders for existing customers

Add products to orders

View order details

Confirm or cancel orders

Order lifecycle with statuses

Business logic validation

Prevents creating orders for inactive customers

Prevents adding items to invalid order states

Automatically updates product stock

Restores stock when an order is canceled

🛠 Tech Stack

Python 3.10+

FastAPI

SQLite

Pydantic

Uvicorn

⚙️ Project Setup

Clone the repository:

git clone https://github.com/the-magister-yoda/crm-api.git
cd crm-api


Install dependencies:

pip install fastapi uvicorn


Run the server:

uvicorn api.main:app --reload


The API will be available at:
👉 http://127.0.0.1:8000

Swagger documentation:
👉 http://127.0.0.1:8000/docs

📌 API Overview
👤 Customers

Create customer

POST /customers

{
  "name": "Daniyar",
  "phone": "+7 777 777 77 77"
}


Get all customers

GET /customers


Get all customers (including inactive)

GET /customers?search=all


Get customer by ID

GET /customers/{customer_id}


Update customer

PATCH /customers/{customer_id}

{
  "name": "New name",
  "phone": "New phone number"
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

📋 Business Rules

You cannot:

Create an order for a non-existent or inactive customer

Add items to an order that is not in created status

Cancel a paid order

Additional rules:

Product stock decreases when items are added to an order

Product stock is restored when an order is canceled

🔖 Statuses

Customer statuses

active

inactive

Order statuses

created

confirmed

paid

canceled

📌 Notes

This project focuses on:

clean API design

validation and business rules

clear separation of concerns

It can be extended with authentication, roles, and integrations.

