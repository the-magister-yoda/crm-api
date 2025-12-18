from fastapi import FastAPI
from database import Database


app = FastAPI()
db = Database()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/customers")
def show_customers():
    customers = db.show_customers()
    res = []
    for customer in customers:
        res.append({
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone
        })
    return res

