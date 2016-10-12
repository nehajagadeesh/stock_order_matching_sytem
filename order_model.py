import datetime


class Order(object):

    def __init__(self, order_attributes):
        self.__validate_order_details(order_attributes)
        self.order_id = order_attributes[0]
        self.order_time = order_attributes[1]
        self.stock_name = order_attributes[2]
        self.order_action = order_attributes[3].lower()
        self.order_qty = int(order_attributes[4])
        self.stock_value = float(order_attributes[5])

    def __validate_order_details(self, order_attributes):
        """
        validating order id and order_action
        :return:
        """
        if len(order_attributes) != 6:
            raise Exception("Invalid order: missing oder details")

        if not (order_attributes[3].lower() in ["buy", "sell"]):
            raise Exception("Invalid order: order_action ==> buy/sell")
        try:
            float(order_attributes[5])
            int(order_attributes[4])
        except Exception:
            raise Exception("Invalid order: amount and qty should be "
                            "float and int respectivey")

    def convert_order_time_to_datetime(self):
        """

        :return:
        """
        try:
            datetime_obj = datetime.datetime.strptime(self.order_time, "%H:%M")
            return datetime_obj
        except Exception:
            raise Exception("Order time format: H:M (hours:minutes)")

    def compare_orders(self, order_obj_1, reverse=False):
        """
        Comparing two order objects based on (stock_price and then timestamp)

        :param order_obj_1:
        :return:
            -1 if self (order_obj --price or price and time)  < order_obj_1
            1 if self (order obj -- price or price and time) > order_obj_1

        """
        if self.stock_value < order_obj_1.stock_value:
            return_value = -1
        elif self.stock_value > order_obj_1.stock_value:
            return_value = 1
        else:
            # if stock price of both are equal then timestamps of the order
            # objects are compared
            if (self.convert_order_time_to_datetime() <=
                    order_obj_1.convert_order_time_to_datetime()):
                comparison = -1
            else:
                comparison = 1
            return_value = comparison * -1 if reverse else comparison
        return return_value
