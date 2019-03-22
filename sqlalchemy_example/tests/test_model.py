import unittest
import sqlalchemy
from sqlalchemy import func
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
