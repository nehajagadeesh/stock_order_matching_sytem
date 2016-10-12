import unittest
from test_order_matching import OrderMatchingTest
from test_order_model import OrderModelTestCase
from test_stock_model import StockTest


def test_suite():
    final_test_suite = unittest.TestSuite()
    final_test_suite.addTests(unittest.makeSuite(OrderModelTestCase))
    final_test_suite.addTests(unittest.makeSuite(StockTest))
    final_test_suite.addTests(unittest.makeSuite(OrderMatchingTest))
    return final_test_suite


def main():
    result = unittest.TextTestRunner().run(test_suite())
    print result
