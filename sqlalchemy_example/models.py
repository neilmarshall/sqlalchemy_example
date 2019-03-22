from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):

    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False)

    # each category can contain zero, one or many products, i.e. a one-to-many
    # relationship where parent = Category and child = Product
    products = relationship('Product', back_populates='category')


class Brand(Base):

    __tablename__ = 'brand'

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String(255), nullable=False)

    # each brand can contain zero, one or many products, i.e. a one-to-many
    # relationship where parent = Brand and child = Product
    products = relationship('Product', back_populates='brand')


class Product(Base):

    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    brand_id = Column(Integer, ForeignKey(Brand.brand_id), nullable=False)
    category_id = Column(Integer, ForeignKey('category.category_id'), nullable=False)
    model_year = Column(Integer, nullable=False)
    list_price = Column(Float, nullable=False)

    # each product belongs to only one category, i.e. a one-to-many
    # relationship where parent = Category and child = Product
    category = relationship('Category', back_populates='products')

    # each product belongs to only one brand, i.e. a one-to-many
    # relationship where parent = Brand and child = Product
    brand = relationship('Brand', back_populates='products')

    # each product conrtains many order items, i.e. a one-to-many
    # relationship where parent = Product and child = Order_Item
    order_items = relationship('Order_Item', back_populates='product')


class Customer(Base):

    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone = Column(String(25))
    email = Column(String(255), nullable=False)
    street = Column(String(255))
    city = Column(String(50))
    state = Column(String(25))
    zip_code = Column(String(5))

    # each customer can contain zero, one or many orders, i.e. a one-to-many
    # relationship where parent = Customer and child = Order
    orders = relationship('Order', back_populates='customer')


class Store(Base):

    __tablename__ = 'store'

    store_id = Column(Integer, primary_key=True)
    store_name = Column(String(255), nullable=False)
    phone = Column(String(25))
    email = Column(String(255))
    street = Column(String(255))
    city = Column(String(255))
    state = Column(String(10))
    zip_code = Column(String(5))

    # each brand can contain zero, one or many products, i.e. a one-to-many
    # relationship where parent = Brand and child = Product
    staff = relationship('Staff', back_populates='store')

    # each store can contain zero, one or many orders, i.e. a one-to-many
    # relationship where parent = Store and child = Order
    orders = relationship('Order', back_populates='store')

    # each store contains stock values for each product, i.e. a one-to-many
    # relationship where parent = Store and child = Stock
    stocks = relationship('Stock', back_populates='store')


class Staff(Base):

    __tablename__ = 'staff'

    staff_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(25))
    active = Column(Integer, nullable=False)
    store_id = Column(Integer, ForeignKey(Store.store_id), nullable=False)
    manager_id = Column(Integer, ForeignKey('staff.staff_id'))

    # each staff member belongs to only one store, i.e. a one-to-many
    # relationship where parent = Store and child = Staff
    store = relationship('Store', back_populates='staff')

    # each staff member has one manager, i.e. a one-to-many
    # relationship where parent = Staff and child = Staff
    manager = relationship('Staff', remote_side=[staff_id])

    # each staff member can contain zero, one or many orders, i.e. a one-to-many
    # relationship where parent = Staff and child = Order
    orders = relationship('Order', back_populates='staff')


class Order(Base):

    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.customer_id))
    order_status = Column(Integer, nullable=False)
    order_date = Column(Date, nullable=False)
    required_date = Column(Date, nullable=False)
    shipped_date = Column(Date)
    store_id = Column(Integer, ForeignKey(Store.store_id), nullable=False)
    staff_id = Column(Integer, ForeignKey(Staff.staff_id), nullable=False)

    # each order belongs to only one customer, i.e. a one-to-many
    # relationship where parent = Customer and child = Order
    customer = relationship('Customer', back_populates='orders')

    # each order belongs to only one store, i.e. a one-to-many
    # relationship where parent = Store and child = Order
    store = relationship('Store', back_populates='orders')

    # each order belongs to only one staff member, i.e. a one-to-many
    # relationship where parent = Staff and child = Order
    staff = relationship('Staff', back_populates='orders')

    # each order relates to exactly one order_item, i.e. a one-to-one
    # relationship where parent = Order and child = Order_Item
    order_item = relationship('Order_Item', uselist=False, back_populates='order')

class Order_Item(Base):

    __tablename__ = 'order_item'

    order_id = Column(Integer, ForeignKey(Order.order_id), primary_key=True)
    item_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.product_id), nullable=False)
    quantity = Column(Integer, nullable=False)
    list_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False, default=0)

    # each order item relates to exactly one order, i.e. a one-to-one
    # relationship where parent = Order and child = Order_Item
    order = relationship('Order', back_populates='order_item')

    # each order item corresponds to a single product, i.e. a one-to-many
    # relationship where parent = Product and child = Order_Item
    product = relationship('Product', back_populates='order_items')


class Stock(Base):

    __tablename__ = 'stock'

    store_id = Column(Integer, ForeignKey(Store.store_id), primary_key=True)
    product_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    # each stock value corresponds to a single store, i.e. a one-to-many
    # relationship where parent = Store and child = Stock
    store = relationship('Store', back_populates='stocks')
