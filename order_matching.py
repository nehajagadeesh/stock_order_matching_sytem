from order_model import Order
from stock_model import Stock


class OrderMatching(object):

    def __init__(self):
        self.orders_list = []
        self.final_data = {}
        self.matched_queries = []

    @staticmethod
    def get_input():
        """
        Retrive the stock input from the user
        :return:
        """
        orders_list = []
        print "Enter the details of the orders:"
        while True:
            single_order = raw_input()
            if not single_order.strip():
                break
            else:
                orders_list.append(single_order)
        return orders_list

    def populate_order_matches(self, orders_list):
        """
        generate the matched orders based on user input.
        Each stock is represented as a key of the dictionary with value being a
        stock object that has a buy and sell list
        :param orders_list:
        :return:
        """
        matched_queries = []
        for order_str in orders_list:
            order_details = order_str.split(" ")
            order_obj = Order(order_details)
            stock_name = order_details[2].lower()
            if stock_name not in self.final_data:
                self.final_data[stock_name] = Stock(stock_name)
            self.final_data[stock_name].match_order_queries(
                order_obj, matched_queries)
        self.matched_queries = matched_queries
        print "The matched orders are in the order:"
        print "\n".join(matched_queries)

    def main(self):
        orders = OrderMatching.get_input()
        self.populate_order_matches(orders)

