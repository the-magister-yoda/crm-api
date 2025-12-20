from datetime import date, datetime


class Customer:
    def __init__(self, name, phone, id=None, status='active'):
        self.id = id
        self.name = name
        self.phone = phone
        self.status = status


    def __str__(self):
        return f'id: {self.id} | name: {self.name} | phone: {self.phone} | status: {self.status}'



class Goods:
    def __init__(self, name, price, quantity, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity


    def __str__(self):
        return f'id: {self.id} | name: {self.name} | price: {self.price} | quantity {self.quantity}'



class Order:
    def __init__(self, customer_id, status='created', id=None):
        self.id = id
        self.customer_id = customer_id
        self.created_at = datetime.now()
        self.status = status


    def __str__(self):
        return f'id: {self.id} | customer_id: {self.customer_id} | created at: {self.created_at} | :status: {self.status}'