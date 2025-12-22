import sqlite3 as sq

from errors import CustomerNotFound, CustomerInactive, CustomerEmpty, OrderNotFound, NotEnoughQuantity, OrderInactive, ProductNotFound, OrderAlreadyPaid
from models import Customer, Goods, Order



class Database:
    def __init__(self):
        self.conn = sq.connect(
            'pg_crm_flowers.db',
            check_same_thread=False
        )
        self.cursor = self.conn.cursor()
        self.create_schema()


    def create_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  status TEXT NOT NULL
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
            INSERT INTO customers(name, phone, status) VALUES(?, ?, ?)
            """, (customer.name, customer.phone, customer.status))
        self.conn.commit()


    def add_product(self, good):
        self.cursor.execute("""
            INSERT INTO goods(name, price, quantity) VALUES(?,?,?)
        """, (good.name, good.price, good.quantity))
        self.conn.commit()


    def show_customers(self):
        self.cursor.execute("""
            SELECT id, name, phone, status FROM customers
        """)
        rows = self.cursor.fetchall()
        return [Customer(name, phone, id, status) for id, name, phone, status in rows]


    def show_products(self):
        self.cursor.execute("""
            SELECT id, name, price, quantity FROM goods
        """)
        rows = self.cursor.fetchall()
        return [Goods(name, price, quantity, id) for id, name, price, quantity in rows]


    def create_order(self, order):
        self.cursor.execute("""
        SELECT status FROM customers
        WHERE id = ?
        """, (order.customer_id,))
        status = self.cursor.fetchone()

        if status is None:
            raise CustomerNotFound()
        
        if status[0] == 'inactive':
            raise CustomerInactive()
        
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
        SELECT status FROM orders
        WHERE id = ?
        """, (order_id,))
        status = self.cursor.fetchone()

        if status is None:
            raise OrderNotFound()

        if status[0] != 'created':
            raise OrderInactive()

        self.cursor.execute("""
            SELECT price, quantity FROM goods WHERE id = ?
        """, (goods_id,))

        row = self.cursor.fetchone()
        if row is None:
            raise ProductNotFound()

        price, current_quantity = row

        if current_quantity < quantity:
            raise NotEnoughQuantity()

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
         SELECT status FROM orders
         WHERE id = ?                 
        """, (order_id,))
        status = self.cursor.fetchone()

        if status is None:
            raise OrderNotFound()
        
        if status[0] == 'canceled':
            raise OrderInactive()
        

        self.cursor.execute("""
            SELECT g.name, oi.quantity, oi.price, (oi.quantity * oi.price) AS total
            FROM order_items oi
            JOIN goods g ON g.id = oi.goods_id
            WHERE oi.order_id = ?
        """, (order_id,))
        rows = self.cursor.fetchall()
        return [
                    {
                        "name": row[0],
                        "quantity": row[1],
                        "price": row[2],
                        "total": row[3],
                    }
                    for row in rows
                ]


    def show_total(self):
        self.cursor.execute("""
            SELECT SUM(oi.quantity * oi.price) 
            FROM order_items oi
            JOIN orders o ON  o.id = oi.order_id
            WHERE o.status = 'paid'
        """)
        total = self.cursor.fetchone()
        return total[0] if total[0] is not None else 0


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
            raise OrderNotFound()

        status = row[0]

        if status == 'paid':
            raise OrderAlreadyPaid()

        self.cursor.execute("""
            SELECT goods_id, quantity 
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))

        items = self.cursor.fetchall()
        if not items:
            raise ProductNotFound()

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
        """, (order_id,))
        self.conn.commit()

    
    def get_customer(self, id):
        self.cursor.execute("""
            SELECT name, phone FROM customers
            WHERE id = ?
        """, (id,))
        data = self.cursor.fetchone()
        if data is None:
            raise ValueError('Customer not found')
        
        name, phone = data
        
        return Customer(name, phone, id)
    

    def update_customer(self, id, name=None, phone=None):
        self.cursor.execute("""
            SELECT status FROM customers
            WHERE id = ?
        """, (id,))
        data = self.cursor.fetchone()

        if data is None:
            raise CustomerNotFound()
        
        status = data[0]

        if status == 'inactive':
            raise CustomerInactive()
        
        if name is None and phone is None:
            raise CustomerEmpty()

        if name is not None:
            self.cursor.execute("""
                UPDATE customers
                SET name = ?
                WHERE id = ?
            """, (name, id))

        if phone is not None:
            self.cursor.execute("""
                UPDATE customers
                SET phone = ?
                WHERE id = ?
            """, (phone, id))
        self.conn.commit()

        self.cursor.execute("""
            SELECT name, phone FROM customers
            WHERE id = ?
        """, (id,))
        info = self.cursor.fetchone()
        name, phone = info

        return Customer(name, phone, status, id)

    

    def delete_customer(self, id):
        self.cursor.execute("""
            SELECT id, name, phone, status FROM customers
            WHERE id = ?
        """, (id,))
        data = self.cursor.fetchone()

        if data is None:
            raise ValueError
        
        id, name, phone, status = data

        if status == 'inactive':
            raise ValueError

        self.cursor.execute("""
            UPDATE customers
            SET status = 'inactive'
            WHERE id = ?
        """, (id,))
        self.conn.commit()
        return Customer(name, phone, status, id)
    

    def confirm_order(self, order_id):
        self.cursor.execute("""
            SELECT status FROM orders
            WHERE id = ?           
        """, (order_id,))
        status = self.cursor.fetchone()

        if status is None:
            raise OrderNotFound()
        
        if status[0] != 'created':
            raise ValueError('Order cannot be confirmed')
        

        self.cursor.execute("""
            SELECT goods_id FROM order_items
            WHERE order_id = ?
        """,(order_id,))
        goods = self.cursor.fetchone()

        if goods is None:
            raise ProductNotFound()
        
        self.cursor.execute("""
            UPDATE orders
            SET status = 'confirmed'
            WHERE id = ?
        """,(order_id,))
        self.conn.commit()
       
        
    
        





