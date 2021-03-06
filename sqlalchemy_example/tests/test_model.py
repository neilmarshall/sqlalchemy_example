import unittest
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from sqlalchemy_example.create_session import *

class TestQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = build_session()

    def test_database_created_successfully(self):
        self.assertTrue(isinstance(self.session, sqlalchemy.orm.session.Session))

    def test_select_all_from_customers_returns_correct_data(self):
        results = self.session.query(Customer).all()
        self.assertEqual(len(results), 1445)
        self.assertEqual(results[0].first_name, 'Debra')
        self.assertEqual(results[0].last_name, 'Burks')
        self.assertEqual(results[0].email, 'debra.burks@yahoo.com')

    def test_select_columns_from_customers_returns_correct_data(self):
        results = self.session.query(Customer.first_name, Customer.last_name).all()
        self.assertEqual(len(results), 1445)
        self.assertEqual(results[0], ('Debra', 'Burks'))

    def test_select_columns_from_customers_with_sort_returns_correct_data(self):
        result = self.session.query(Customer.first_name, Customer.last_name) \
                             .order_by(Customer.last_name).first()
        self.assertEqual(result, ('Jamika', 'Acevedo'))

    def test_select_columns_from_customers_with_filter_and_sort_returns_correct_data(self):
        results = self.session.query(Customer.first_name, Customer.last_name) \
                              .filter_by(state = 'CA') \
                              .order_by(Customer.last_name).all()
        self.assertEqual(len(results), 284)
        self.assertEqual(results[0], ('Ester', 'Acevedo'))

    def test_groupby_returns_correctly(self):
        results = self.session.query(Customer.city, func.count(Customer.city)) \
                              .filter_by(state = 'CA') \
                              .group_by(Customer.city) \
                              .order_by(Customer.city) \
                              .all()
        self.assertEqual(len(results), 40)
        self.assertEqual(results[0], ('Anaheim', 11))
        self.assertEqual(results[-1], ('Yuba City', 1))

    def test_groupby_with_filter_returns_correctly(self):
        city_count = self.session.query(Customer.city, func.count(Customer.city).label('city_count')) \
                                 .filter_by(state = 'CA') \
                                 .group_by(Customer.city) \
                                 .subquery()
        results = self.session.query(city_count) \
                              .filter(city_count.c.city_count > 10) \
                              .order_by(city_count.c.city) \
                              .all()
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0], ('Anaheim', 11))
        self.assertEqual(results[-1], ('Upland', 11))


class TestAdvancedQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = build_session()

    def test_select_distinct(self):
        count = self.session.query(Customer.city).distinct().count()
        self.assertEqual(count, 195)

    def test_select_multiple_columns_with_multiple_filters(self):
        results = self.session.query(Product.product_id,
                                     Product.product_name,
                                     Product.category_id,
                                     Product.model_year,
                                     Product.list_price) \
                              .filter_by(category_id = 1, model_year = 2018) \
                              .order_by(Product.list_price.desc(), Product.product_id) \
                              .all()
        self.assertEqual(len(results), 37)
        self.assertEqual(results[0],
            (280, "Trek Superfly 24 - 2017/2018", 1, 2018, 489.99))

    def test_select_multiple_columns_with_like_operator(self):
        results = self.session.query(Product.product_id,
                                     Product.product_name,
                                     Product.category_id,
                                     Product.model_year,
                                     Product.list_price) \
                              .filter(Product.product_name.like('%Cruiser%')) \
                              .order_by(Product.list_price.desc(), Product.product_id) \
                              .all()
        self.assertEqual(len(results), 19)
        self.assertEqual(results[0],
            (233, "Electra Cruiser Lux Fat Tire 7D - 2018", 3, 2018, 639.99))

    def test_select_multiple_columns_with_in_operator(self):
        results = self.session.query(Product.product_name,
                                     Product.list_price) \
                              .filter(Product.list_price.in_([89.99, 109.99, 159.99])) \
                              .order_by(Product.list_price) \
                              .all()
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0],
            ("Strider Classic 12 Balance Bike - 2018", 89.99))


class TestQueriesWithNull(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = build_session()

    def test_select_null_values(self):
        results = self.session.query(Customer.customer_id,
                                     Customer.first_name,
                                     Customer.last_name,
                                     Customer.phone) \
                              .filter(Customer.phone.is_(None)) \
                              .order_by(Customer.first_name, Customer.last_name) \
                              .all()
        self.assertEqual(len(results), 1267)
        self.assertEqual(results[0], (338, 'Abbey', 'Pugh', None))

    def test_select_not_null_values(self):
        results = self.session.query(Customer.customer_id,
                                     Customer.first_name,
                                     Customer.last_name,
                                     Customer.phone) \
                              .filter(~Customer.phone.is_(None)) \
                              .order_by(Customer.first_name, Customer.last_name) \
                              .all()
        self.assertEqual(len(results), 178)
        self.assertEqual(results[0], (1174, 'Aaron', 'Knapp', '(914) 402-4335'))


class TestReturnValues(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = build_session()

    def test_all_method_returns_list_of_all_results(self):
        results = self.session.query(Brand).all()
        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 9)

    def test_first_method_returns_scalar(self):
        result = self.session.query(Brand).filter_by(brand_name = 'Electra').first()
        self.assertEqual((result.brand_id, result.brand_name), (1, 'Electra'))

    def test_one_method_with_one_result_returns_correctly(self):
        result = self.session.query(Brand).filter_by(brand_name = 'Electra').one()
        self.assertEqual((result.brand_id, result.brand_name), (1, 'Electra'))

    def test_one_method_with_no_results_errors(self):
        query = self.session.query(Brand).filter_by(brand_name = None).one
        self.assertRaises(NoResultFound, query)

    def test_one_method_with_multiple_results_errors(self):
        query = self.session.query(Brand).one
        self.assertRaises(MultipleResultsFound, query)

    def test_one_or_none_method_with_one_result_returns_correctly(self):
        result = self.session.query(Brand).filter_by(brand_name = 'Electra').one_or_none()
        self.assertEqual((result.brand_id, result.brand_name), (1, 'Electra'))

    def test_one_or_none_method_wht_no_results_returns_None(self):
        result = self.session.query(Brand).filter_by(brand_name = None).one_or_none()
        self.assertIsNone(result)

    def test_one_or_none_method_with_multiple_results_errors(self):
        query = self.session.query(Brand).one_or_none
        self.assertRaises(MultipleResultsFound, query)

    def test_scalar_method_returns_correctly(self):
        result = self.session.query(Customer.first_name, Customer.last_name) \
                             .filter_by(customer_id = 1) \
                             .scalar()
        self.assertEqual(result, 'Debra')

    def test_scalar_method_with_no_results_returns_None(self):
        result = self.session.query(Brand).filter_by(brand_name = None).scalar()
        self.assertIsNone(result)

    def test_scalar_method_with_multiple_results_errors(self):
        query = self.session.query(Brand).scalar
        self.assertRaises(MultipleResultsFound, query)


class TestForeignKeyConstraints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = build_session()

    def setUp(self):
        self.session.rollback()  # needed as this test class raises errors that need to be flushed

    def test_adding_product_with_nonexistent_brand_id_errors(self):
        new_product = Product(product_name='test',
                              brand_id=99999,
                              category_id=1,
                              model_year=2019,
                              list_price=999.99)
        self.session.add(new_product)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_adding_product_with_nonexistent_category_id_errors(self):
        new_product = Product(product_name='test',
                              brand_id=1,
                              category_id=99999,
                              model_year=2019,
                              list_price=999.99)
        self.session.add(new_product)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_deleting_brand_id_that_exists_in_a_product_errors(self):
        brand = self.session.query(Brand).first()
        self.session.delete(brand)
        self.assertRaises(IntegrityError, self.session.commit)

