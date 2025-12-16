import sqlite3 as sq

from models import Customer, Goods, Order



class Database:
    def __init__(self):
        self.conn = sq.connect('pg_crm_flowers.db')
        self.cursor = self.conn.cursor()
        self.create_schema()


    def create_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS goods (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  price REAL NOT NULL,
                  quantity INTEGER NOT NULL
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  customer_id INTEGER NOT NULL,
                  created_at TEXT NOT NULL,
                  status TEXT NOT NULL,
                  FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                goods_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY(order_id) REFERENCES orders(id),
                FOREIGN KEY(goods_id) REFERENCES goods(id)
            )
        """)

        self.conn.commit()


    def add_customer(self, customer):
        self.cursor.execute("""
            INSERT INTO customers(name, phone) VALUES(?, ?)
            """, (customer.name, customer.phone))
        self.conn.commit()


    def add_product(self, good):
        self.cursor.execute("""
            INSERT INTO goods(name, price, quantity) VALUES(?,?,?)
        """, (good.name, good.price, good.quantity))
        self.conn.commit()


    def show_customers(self):
        self.cursor.execute("""
            SELECT id, name, phone FROM customers
        """)
        rows = self.cursor.fetchall()
        return [Customer(name, phone, id) for id, name, phone in rows]


    def show_products(self):
        self.cursor.execute("""
            SELECT id, name, price, quantity FROM goods
        """)
        rows = self.cursor.fetchall()
        return [Goods(name, price, quantity, id) for id, name, price, quantity in rows]


    def create_order(self, order):
        order.status = 'created'
        self.cursor.execute("""
            INSERT INTO orders(customer_id, created_at, status) VALUES(?, ?, ?)
            """, (order.customer_id, order.created_at.isoformat(), order.status))
        self.conn.commit()
        return self.cursor.lastrowid


    def show_orders(self):
        self.cursor.execute("""
            SELECT id, customer_id, created_at, status FROM orders
        """)
        rows = self.cursor.fetchall()
        return [Order(customer_id, created_at, status, id) for id, customer_id, created_at, status in rows]


    def add_order_details(self, order_id, goods_id, quantity):
        self.cursor.execute("""
            SELECT price, quantity FROM goods WHERE id = ?
        """, (goods_id,))

        row = self.cursor.fetchone()
        if row is None:
            raise ValueError('Product not found')

        price, current_quantity = row

        if current_quantity < quantity:
            raise ValueError("Not enough goods in stock")

        self.cursor.execute("""
            INSERT INTO order_items(order_id, goods_id, quantity, price) 
            VALUES(?, ?, ?, ?)
        """, (order_id, goods_id, quantity, price))

        self.cursor.execute("""
            UPDATE goods
            SET quantity = quantity - ?
            WHERE id = ?
        """, (quantity, goods_id))
        self.conn.commit()


    def show_order_details(self, order_id):
        self.cursor.execute("""
            SELECT g.name, oi.quantity, oi.price, (oi.quantity * oi.price) AS total
            FROM order_items oi
            JOIN goods g ON g.id = oi.goods_id
            WHERE oi.order_id = ?
        """, (order_id,))
        return self.cursor.fetchall()


    def show_total(self):
        self.cursor.execute("""
            SELECT (quantity * price) AS total
            FROM order_items 
        """)
        return self.cursor.fetchall()


    def pay_for_order(self, order_id):
        self.cursor.execute("""
            SELECT status FROM orders
            WHERE id = ?
        """, (order_id,))

        row = self.cursor.fetchone()
        if row is None:
            raise ValueError('Order is not found')

        status = row[0]

        if status == 'paid':
            raise ValueError('Order already paid')

        status = 'paid'

        self.cursor.execute("""
            UPDATE orders
            SET status = ?
            WHERE id = ?
        """, (status, order_id))
        self.conn.commit()


    def cancel_order(self, order_id):
        self.cursor.execute("""
            SELECT status FROM orders
            WHERE id = ?
        """, (order_id,))

        row = self.cursor.fetchone()

        if row is None:
            raise ValueError('Order not found')

        status = row[0]

        if status == 'paid':
            raise ValueError('Order already paid it cant ba canceled')

        self.cursor.execute("""
            SELECT goods_id, quantity 
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))

        items = self.cursor.fetchall()
        if not items:
            raise ValueError('Order has no items')

        for goods_id, quantity in items:
            self.cursor.execute("""
                UPDATE goods
                SET quantity = quantity + ?
                WHERE id = ?
            """, (quantity, goods_id))

        self.cursor.execute("""
            UPDATE orders
            SET status = 'canceled'
            WHERE id = ?
        """, (status, order_id))
        self.conn.commit()





