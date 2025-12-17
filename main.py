from datetime import date, datetime
from database import Database
from models import Customer, Goods, Order



class Crm:
    def __init__(self):
        self.db = Database()


    def add_customer(self, customer: Customer):
        self.db.add_customer(customer)
        print('Customer added ')


    def add_product(self, good: Goods):
        self.db.add_product(good)
        print('Product added ')


    def create_order(self, order: Order):
        order_id = self.db.create_order(order)
        print(f'Заказ создан, id = {order_id}')
        return order_id


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
        try:
            self.db.add_order_details(order_id, goods_id, quantity)
            print("Product added to order")
        except ValueError as e:
            print(f'Error: {e}')


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
        print(f"Total: {total_sum}\n")


    def show_total(self):
        total = self.db.show_total()
        print('Общая сумму оплаченных заказов:')
        print(total)


    def pay_for_order(self, order_id):
        try:
            self.db.pay_for_order(order_id)
            print('Paid successfully ')
        except ValueError as e:
            print(f'Error: {e}')


    def cancel_order(self, order_id):
        try:
            self.db.cancel_order(order_id)
            print('Order canceled')
        except ValueError as e:
            print(f'Error: {e}')





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
    print("8. Pay for order ")
    print("9. Cancel order ")
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

        created_at = datetime.now()
        status = 'new'
        order = Order(customer_id, created_at, status)
        order_id = crm.create_order(order)

        while True:
            crm.show_products()
            goods_id = int(input('Enter id of product (0 to finish): '))
            if goods_id == 0:
                break

            quantity = int(input('Enter quantity: '))
            crm.add_order_details(order_id, goods_id, quantity)


    elif choice == '4':
        crm.show_customers()


    elif choice == '5':
        crm.show_products()


    elif choice == '6':
        crm.show_orders()
        order_id = int(input('Enter id of order you want to see: '))

        crm.show_order_details(order_id)


    elif choice == '7':
        crm.show_total()


    elif choice == '8':
        crm.show_orders()
        order_id = int(input('Enter id of order you want to pay: '))

        crm.pay_for_order(order_id)


    elif choice == '9':
        crm.show_orders()
        order_id = int(input('Enter id of order you want to cancel: '))

        crm.cancel_order(order_id)


