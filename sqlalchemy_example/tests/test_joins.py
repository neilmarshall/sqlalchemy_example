import unittest
import sqlalchemy

from sqlalchemy_example.create_session import *

class TestJoins(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = build_session()

    def test_inner_join_on_related_tables(self):
        results = self.session.query(Product.product_name,
                                     Category.category_name,
                                     Product.list_price) \
                              .filter(Product.category_id==Category.category_id) \
                              .order_by(Product.product_name.desc()) \
                              .all()
        self.assertEqual(len(results), 321)
        self.assertEqual(results[0],
            ("Trek XM700+ Lowstep - 2018", "Electric Bikes", 3499.99))

    def test_left_join_on_related_tables(self):
        results = self.session.query(Product.product_name,
                                     Order_Item.order_id) \
                              .outerjoin(Order_Item) \
                              .order_by(Order_Item.order_id, Product.product_name) \
                              .all()
        self.assertEqual(len(results), 4736)
        self.assertEqual(results[0],
            ("Electra Savannah 1 (20-inch) - Girl's - 2018", None))


class TestObjectRelations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = build_session()

    def test_object_relationship_between_Category_and_Product(self):
        results = self.session.query(Category) \
                      .filter_by(category_id = 1) \
                      .one() \
                      .products
        products = sorted(r.product_name for r in results)
        self.assertEqual(len(products), 59)
        self.assertEqual(products[0], "Electra Cruiser 1 (24-Inch) - 2016")
