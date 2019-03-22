from datetime import datetime
from sqlalchemy_example.models import *

def load_categories(session):
    for category_id, category_name in [(1,'Children Bicycles'), (2,'Comfort Bicycles'),
                                       (3,'Cruisers Bicycles'), (4,'Cyclocross Bicycles'),
                                       (5,'Electric Bikes'), (6,'Mountain Bikes'),
                                       (7,'Road Bikes')]:
        category = Category(category_id=category_id, category_name=category_name)
        session.add(category)
    session.commit()


def load_brands(session):
    for brand_id, brand_name in [(1, 'Electra'), (2, 'Haro'), (3, 'Heller'),
                                 (4, 'Pure Cycles'), (5, 'Ritchey'), (6, 'Strider'),
                                 (7, 'Sun Bicycles'), (8, 'Surly'), (9, 'Trek')]:
        brand = Brand(brand_id=brand_id, brand_name=brand_name)
        session.add(brand)
    session.commit()


def load_products(session):
    with open('sqlalchemy_example/data/products.csv', 'r') as datafile:
        for line in datafile:
            product_id, product_name, brand_id, category_id, model_year, list_price = line.split(',')
            product = Product(product_id=product_id,
                              product_name=product_name,
                              brand_id=brand_id,
                              category_id=category_id,
                              model_year=model_year,
                              list_price=list_price)
            session.add(product)
    session.commit()


def load_customers(session):
    with open('sqlalchemy_example/data/customers.csv', 'r') as datafile:
        for line in datafile:
            data = map(lambda x: x if x != 'NULL' else None, line.split(','))
            first_name, last_name, phone, email, street, city, state, zip_code = data
            customer = Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                street=street,
                                city=city,
                                state=state,
                                zip_code=zip_code)
            session.add(customer)
    session.commit()


def load_stores(session):
    for store_name, phone, email, street, city, state, zip_code in [
        ('Santa Cruz Bikes', '(831) 476-4321', 'santacruz@bikes.shop', '3700 Portola Drive',  'Santa Cruz', 'CA', '95060'),
        ('Baldwin Bikes', '(516) 379-8888', 'baldwin@bikes.shop', '4200 Chestnut Lane',  'Baldwin', 'NY', '11432'),
        ('Rowlett Bikes', '(972) 530-5555', 'rowlett@bikes.shop', '8000 Fairway Avenue',  'Rowlett', 'TX', '75088')]:
        store = Store(store_name=store_name,
                      phone=phone,
                      email=email,
                      street=street,
                      city=city,
                      state=state,
                      zip_code=zip_code)
        session.add(store)
    session.commit()


def load_stocks(session):
    with open('sqlalchemy_example/data/stocks.csv', 'r') as datafile:
        for line in datafile:
            store_id, product_id, quantity = line.split(',')
            stock = Stock(store_id=store_id,
                          product_id=product_id,
                          quantity=quantity)
            session.add(stock)
    session.commit()


def load_staff(session):
    for staff_id, first_name, last_name, email, phone, active, store_id, manager_id in [
            (1,'Fabiola','Jackson','fabiola.jackson@bikes.shop','(831) 555-5554',1,1,None),
            (2,'Mireya','Copeland','mireya.copeland@bikes.shop','(831) 555-5555',1,1,1),
            (3,'Genna','Serrano','genna.serrano@bikes.shop','(831) 555-5556',1,1,2),
            (4,'Virgie','Wiggins','virgie.wiggins@bikes.shop','(831) 555-5557',1,1,2),
            (5,'Jannette','David','jannette.david@bikes.shop','(516) 379-4444',1,2,1),
            (6,'Marcelene','Boyer','marcelene.boyer@bikes.shop','(516) 379-4445',1,2,5),
            (7,'Venita','Daniel','venita.daniel@bikes.shop','(516) 379-4446',1,2,5),
            (8,'Kali','Vargas','kali.vargas@bikes.shop','(972) 530-5555',1,3,1),
            (9,'Layla','Terrell','layla.terrell@bikes.shop','(972) 530-5556',1,3,7),
            (10,'Bernardine','Houston','bernardine.houston@bikes.shop','(972) 530-5557',1,3,7)]:
        staff = Staff(staff_id=staff_id,
                      first_name=first_name,
                      last_name=last_name,
                      email=email,
                      phone=phone,
                      active=active,
                      store_id=store_id,
                      manager_id=manager_id)
        session.add(staff)
    session.commit()


def load_orders(session):
    with open('sqlalchemy_example/data/orders.csv', 'r') as datafile:
        for line in datafile:
            # 1,259,4,'20160101','20160103','20160103',1,2
            order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id = line.split(',')
            order_date = datetime.strptime(order_date, '%Y%m%d')
            required_date = datetime.strptime(required_date, '%Y%m%d')
            shipped_date = datetime.strptime(shipped_date, '%Y%m%d')if shipped_date != 'NULL' else None
            order = Order(order_id=order_id,
                          customer_id=customer_id,
                          order_status=order_status,
                          order_date=order_date,  # DATE
                          required_date=required_date,  # DATE
                          shipped_date=shipped_date,  # DATE
                          store_id=store_id,
                          staff_id=staff_id)
            session.add(order)
    session.commit()


def load_order_items(session):
    with open('sqlalchemy_example/data/order_items.csv', 'r') as datafile:
        for line in datafile:
            order_id, item_id, product_id, quantity, list_price, discount = line.split(',')
            order_item = Order_Item(order_id=order_id,
                                    item_id=item_id,
                                    product_id=product_id,
                                    quantity=quantity,
                                    list_price=list_price,
                                    discount=discount)
            session.add(order_item)
    session.commit()
