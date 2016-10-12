from stock_model import Stock
from order_model import Order
import unittest


class StockTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_insert_ascending_order(self):
        order_list = [
            Order("#3 9:45 XAM sell 100 240.10".split(" ")),
            Order("#2 9:40 XAM sell 100 245.10".split(" ")),
            Order("#1 9:41 XAM sell 100 240.10".split(" ")),
            Order("#4 9:41 XAM sell 100 240.10".split(" ")),
            Order("#5 9:41 XAM sell 100 239.10".split(" "))]

        stock_obj = Stock("xam")
        with self.assertRaises(Exception) as exc:
            stock_obj._insert_in_ascending_order(order_list[0], 0, -1)
        self.assertIn("Index", str(exc.exception))

        stock_obj.sorting_queue = [order_list[0], order_list[1]]
        with self.assertRaises(Exception) as exc:
            stock_obj._insert_in_ascending_order(order_list[2], 0, 1)
        self.assertIn("Index", str(exc.exception))

        stock_obj.sorting_queue = [order_list[2], order_list[0], order_list[1]]
        stock_obj._insert_in_ascending_order(order_list[4], 0, 2)
        stock_obj._insert_in_ascending_order(order_list[3], 0, 3)

        compare_list = [order.order_id for order in stock_obj.sorting_queue]
        self.assertListEqual(compare_list, ["#5", "#4", "#1", "#3", "#2"])

    def test_insert_into_queue(self):
        queue = []
        order_list = [
            Order("#1 9:41 XAM sell 100 240.10".split(" ")),
            Order("#2 9:40 XAM sell 100 245.10".split(" ")),
            Order("#3 9:45 XAM sell 100 240.10".split(" ")),
            Order("#4 9:41 XAM sell 100 240.10".split(" ")),
            Order("#5 9:41 XAM sell 100 239.10".split(" ")),]

        op_order_list = ["#5", "#4", "#1", "#3", "#2"]
        op_order_list_reverse = ["#5", "#3", "#1", "#4", "#2"]

        stock_obj = Stock("xam")
        for order_obj in order_list:
            stock_obj.insert_into_queue(order_obj, queue)

        queue_extract = [order.order_id for order in queue]
        self.assertListEqual(op_order_list, queue_extract)

        queue = []
        stock_obj.reverse_sort = True
        for order_obj in order_list:
            stock_obj.insert_into_queue(order_obj, queue)

        queue_extract = [order.order_id for order in queue]
        self.assertListEqual(op_order_list_reverse, queue_extract)

    def test_matched_order_queries(self):
        order_list = [
            "#1 09:45 XAM sell 100 240.10",
            "#2 09:45 XAM sell 90 237.45",
            "#3 09:47 XAM buy 80 238.10",
            "#5 09:48 XAM sell 220 241.50",
            "#6 09:49 XAM buy 50 238.50",
            "#8 10:01 XAM sell 20 240.10",
            "#9 10:02 XAM buy 150 242.70"]

        op_matched = ['#2 80 237.45 #3', '#2 10 237.45 #6', '#8 20 240.1 #9',
                      '#1 100 240.1 #9', '#5 30 241.5 #9']
        stock_obj = Stock("xam")
        matched_queries = []
        for order_str in order_list:
            order = Order(order_str.split(" "))
            stock_obj.match_order_queries(order, matched_queries)

        self.assertListEqual(matched_queries, op_matched)

    def test_generate_matched_queries(self):
        stock_obj = Stock("xam")
        matched_queries = []
        stock_obj.sell_list = [
            Order("#2 09:45 XAM sell 50 237.45".split(" ")),
            Order("#3 09:46 XAM sell 50 237.45".split(" ")),
            Order("#1 09:45 XAM sell 100 240.10".split(" "))]

        stock_obj.buy_list = [
            Order("#4 09:47 XAM buy 80 238.10".split(" "))]

        stock_obj.generate_matched_orders("buy", matched_queries)

        expected_op = ['#2 50 237.45 #4', '#3 30 237.45 #4']
        self.assertListEqual(matched_queries, expected_op)
        formatted_sell_list = [order.order_id for order in stock_obj.sell_list]
        self.assertListEqual(formatted_sell_list, ['#3', '#1'])
        self.assertListEqual(stock_obj.buy_list, [])

