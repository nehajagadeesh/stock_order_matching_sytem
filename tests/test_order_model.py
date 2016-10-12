import unittest
import datetime
from order_model import Order


class OrderModelTestCase(unittest.TestCase):

    def test_order_object_initialisation(self):

        faulty_orders = ([
            "#1 09:45 XAM test 100 240.10", # wrong action type (buy/sell)
            "#1 09:45 XAM sell test 240.10", # wrong quantity type
            "#1 09:45 XAM test 100.0 240.10", #wrong qty type (not int)
            "#1 09:45 XAM test 100 test", #wrong amount type
            "#1 09:45 XAM test 100", # missing details
            ])
        for faulty_order_details in faulty_orders:
            with self.assertRaises(Exception) as exc:
                Order(faulty_order_details.split(" "))
            self.assertIn('Invalid order', str(exc.exception))

    def test_conversion_order_time(self):
        correct_orders = ([
            "#1 9:45 XAM sell 100 240.10",
            "#1 09:45 XAM sell 100 240.10",
            "#1 9:1 XAM sell 100 240.10",
        ])
        faulty_orders = ([
            "#1 945 XAM sell 100 240.10",
            "#1 test:4 XAM sell 100 240.10",
            "#1 5:4:9 XAM sell 100 240.10"
        ])
        for order in correct_orders:
            order_obj = Order(order.split(" "))
            self.assertIsInstance(order_obj.convert_order_time_to_datetime(),
                                  datetime.datetime)

        for order in faulty_orders:
            order_obj = Order(order.split(" "))
            with self.assertRaises(Exception) as exc:
                order_obj.convert_order_time_to_datetime()
            self.assertIn("Order time format", str(exc.exception))

    def test_compare_orders(self):
        order_obj = Order("#1 9:41 XAM sell 100 240.10".split(" "))
        order_obj_2 = Order("#2 9:40 XAM sell 100 245.10".split(" "))
        order_obj_3 = Order("#3 9:45 XAM sell 100 240.10".split(" "))
        order_obj_4 = Order("#4 9:41 XAM sell 100 240.10".split(" "))

        """
        print "order 1 : #1 9:41 XAM sell 100 240.10"
        print "order 2 : #2 9:40 XAM sell 100 245.10"
        print "order 3 : #3 9:45 XAM sell 100 240.10"

        print "order1 < order2"
        """
        self.assertEqual(order_obj.compare_orders(order_obj_2), -1)
        self.assertEqual(order_obj.compare_orders(order_obj_2, True), -1)

        """
        print ("check order1 < order3 (same value, order 1 has better time "
               "priority")
        """
        self.assertEqual(order_obj.compare_orders(order_obj_3), -1)
        self.assertEqual(order_obj.compare_orders(order_obj_3, True), 1)

        """
        print ("check order1 < order4 (same value, same time)\n"
               "check order1 > order4 (with reverse_sort true)")
        """
        self.assertEqual(order_obj.compare_orders(order_obj_4), -1)
        self.assertEqual(order_obj.compare_orders(order_obj_4, True), 1)


