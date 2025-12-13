import sqlite3 as sq

from datetime import date, datetime



class Database:
    def __init__(self):
        self.conn = sq.connect('pg_crm_flower.db')
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
        self.cursor.execute("""
            INSERT INTO orders(customer_id, created_at, status) VALUES(?, ?, ?)
            """, (order.customer_id, order.created_at.isoformat(), order.status))
        self.conn.commit()


    def show_orders(self):
        self.cursor.execute("""
            SELECT id, customer_id, created_at, status FROM orders
        """)
        rows = self.cursor.fetchall()
        return [Order(customer_id, created_at, status, id) for id, customer_id, created_at, status in rows]


    def add_order_items(self,order_id, goods_id, quantity):
        self.cursor.execute("""
            SELECT price FROM goods WHERE id = ?
        """, (goods_id,))
        price = self.cursor.fetchone()[0]

        self.cursor.execute("""
            INSERT INTO order_items(order_id, goods_id, quantity, price) VALUES(?, ?, ?, ?)
        """, (order_id, goods_id, quantity, price))
        self.conn.commit()

    
    def show_total(self):
        self.cursor.execute("""
            SELECT (quantity * price) AS total
            FROM order_items 
        """)
        return self.cursor.fetchall()



class Customer:
    def __init__(self, name, phone, id=None):
        self.id = id
        self.name = name
        self.phone = phone


    def __str__(self):
        return f'id: {self.id} | name: {self.name} | phone: {self.phone}'



class Goods:
    def __init__(self, name, price, quantity, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity


    def __str__(self):
        return f'id: {self.id} | name: {self.name} | price: {self.price} | quantity {self.quantity}'



class Order:
    def __init__(self, customer_id, created_at, status, id=None):
        self.id = id
        self.customer_id = customer_id
        self.created_at = created_at
        self.status = status


    def __str__(self):
        return f'id: {self.id} | customer_id: {self.customer_id} | created at: {self.created_at} | :status: {self.status}'



class Crm:
    def __init__(self):
        self.db = Database()


    def add_customer(self, customer: Customer):
        self.db.add_customer(customer)
        print('Клиент добавлен ')


    def add_product(self, good: Goods):
        self.db.add_product(good)
        print('Продукт добавлен ')


    def create_order(self, order: Order):
        self.db.create_order(order)
        print('Заказ добавлен ')


    def show_customers(self):
        rows = self.db.show_customers()
        for row in rows:
            print(row)


    def show_products(self):
        rows = self.db.show_products()
        for row in rows:
            print(row)


    def show_orders(self):
        rows = self.db.show_orders()
        for row in rows:
            print(row)


    def add_order_details(self, order_id, goods_id, quantity):
        self.db.add_order_details(order_id, goods_id, quantity)


    def show_order_details(self, order_id):
        rows = self.db.show_order_details(order_id)

        if not rows:
            print('There are no goods in order')
            return

        print('Products of order: ')
        print("-------------------------")

        total_sum = 0

        for name, quantity, price, total in rows:
            print(f"{name} | quantity: {quantity} x price: {price} = {total}")
            total_sum += total

        print("-------------------------")
        print(f"Итого: {total_sum}\n")

    
    def show_total(self):
        rows = self.db.show_total()

        total = 0
        for row in rows:
            total += int(*row)

        print(total)



crm = Crm()

while True:
    print("Choose the action: ")
    print("0. Exit ")
    print("1. Add customer ")
    print("2. Add product ")
    print("3. Create order ")
    print("4. Show customers ")
    print("5. Show products ")
    print("6. Show orders ")
    print("7. Total sum of sales ")
    choice = input('Enter the number of action: ')


    if choice == '0':
        break


    elif choice == '1':
        name = input("Enter your name: ")
        phone = input("Enter your phone number: ")
        customer = Customer(name, phone)
        crm.add_customer(customer)


    elif choice == '2':
        name = input('Enter the name of product: ')
        price = float(input('Enter the price of product: '))
        quantity = int(input('Enter the quantity of product: '))
        product = Goods(name, price, quantity)
        crm.add_product(product)


    elif choice == '3':
        crm.show_customers()
        customer_id = int(input('Enter id of the customer: '))

        crm.show_products()
        goods_id = int(input('Enter id of product: '))
        quantity = int(input('Enter quantity: '))

        created_at = datetime.now()
        status = 'new'


        order = Order(customer_id, created_at, status)
        order_id = crm.create_order(order)
        crm.add_order_details(order_id, goods_id, quantity)


    elif choice == '4':
        crm.show_customers()


    elif choice == '5':
        crm.show_products()


    elif choice == '6':
        crm.show_orders()

    
    elif choice == '7':
        crm.show_total()
