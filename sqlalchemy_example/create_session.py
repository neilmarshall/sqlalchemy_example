from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_example.models import Base
from sqlalchemy_example.load_data import *

def build_session():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute('''PRAGMA foreign_keys = ON;''')
    load_categories(session)
    load_brands(session)
    load_products(session)
    load_customers(session)
    load_stores(session)
    load_stocks(session)
    load_staff(session)
    load_orders(session)
    load_order_items(session)
    return session
