class Stock(object):

    def __init__(self, stock_name):
        self.buy_list = []
        self.sell_list = []
        self.sorting_queue = []
        # for future use , currently unused
        self.stock_name = stock_name
        # for buy queue to ensure orders with higher time priority gets
        # preference in case of equal amount of stock
        self.reverse_sort = False

    def match_order_queries(self, order_obj, matched_queries):
        """
        Function generates all the matching order queries and adds the order
        object to the existing buy/sell list
        :param order_obj:
        :param matched_queries:
        :return:
        """
        if order_obj.order_action == "buy":
            self.reverse_sort = True
            max_buy = self.buy_list[-1].stock_value if self.buy_list else 0
            self.buy_list = self.insert_into_queue(order_obj, self.buy_list)
            if max_buy != self.buy_list[-1].stock_value:
                self.generate_matched_orders(order_obj.order_action,
                                             matched_queries)
        else:
            min_sell = self.sell_list[0].stock_value if self.sell_list else 0
            self.sell_list = self.insert_into_queue(order_obj, self.sell_list)
            if min_sell != self.sell_list[0].stock_value:
                self.generate_matched_orders(order_obj.order_action,
                                             matched_queries)

    def insert_into_queue(self, order_obj, queue):
        """
        Function to insert the object in the respective buy/sell list in a
        sorted order
        :param order_obj:
        :param queue: reference to either buy list or sell list
        :return:
        """
        len_queue = len(queue)
        if len_queue == 0:
            queue.append(order_obj)
        elif len_queue in [1, 2]:
            if order_obj.compare_orders(queue[0], self.reverse_sort) < 1:
                queue.insert(0, order_obj)
            elif len_queue == 2 and order_obj.compare_orders(
                    queue[1], self.reverse_sort) < 1:
                queue.insert(1, order_obj)
            else:
                queue.append(order_obj)
        else:
            # create a temporary queue to avoid sending the queue as an
            # argument to the recursive function
            self.sorting_queue = queue
            self._insert_in_ascending_order(order_obj, 0, len_queue-1)
            queue = self.sorting_queue
        return queue

    def _insert_in_ascending_order(self, order_obj, start, end):
        """
        This recursive function combines binary search with insertion sort to
        build a list sorted in ascending order
        Function called only when length of queue is 3 or longer
        :param order_obj:
        :param start:
        :param end:
        :return:
        """
        # boundary cases of the list
        if end < 0:
            raise Exception("Index out of range")
        if start == end:
            if order_obj.compare_orders(self.sorting_queue[start],
                                        self.reverse_sort) == -1:
                self.sorting_queue.insert(start, order_obj)
            else:
                self.sorting_queue.insert(start+1, order_obj)
            return
        elif start < end:
            size = end - start
            mid = start + size/2
            compare_obj_with_mid = (
                order_obj.compare_orders(self.sorting_queue[mid],
                                         self.reverse_sort))
            compare_obj_with_mid1 = (
                order_obj.compare_orders(self.sorting_queue[mid+1],
                                         self.reverse_sort))

            # if order is greater than the order on the left and lesser than
            # the order on the right (base case of recursion)
            if compare_obj_with_mid == 1 and compare_obj_with_mid1 == -1:
                self.sorting_queue.insert(mid+1, order_obj)
                return
            # find the position to be inserted towards the left of the sorted
            # array
            elif compare_obj_with_mid < 1:
                end = mid - 1
                self._insert_in_ascending_order(order_obj, start, end)
            # find the position to insert the order towards the right of the
            # sorted array
            else:
                start = mid + 1
                self._insert_in_ascending_order(order_obj, start, end)

    def generate_matched_orders(self, new_action, matched_queries):
        """
        Function matches a valid buy and sell order and adds them to the
        queue of matched queries
        The rule for matching is :
              FORMULA:  sell_value <= buy_value
        Function is called to match queries only in either of these conditions:
           1.) when a new sell order is obtained that is lesser than the min
                sell order existing
           2.) when a new buy order is obtained higher than the existing
                maximum buy order

        :param new_action:
        :param matched_queries:
        :return:
        """
        if self.sell_list and self.buy_list:
            break_flag = False
            if new_action == "buy":
                # for a new buy order, multipleq ueries from sell list are
                # matched as long as formula holds good
                max_buy_order = self.buy_list[-1]
                completed_sell_orders = 0
                for sell_order in self.sell_list:
                    buy_qty = max_buy_order.order_qty
                    if sell_order.stock_value <= max_buy_order.stock_value:
                        sell_qty = sell_order.order_qty
                        if buy_qty > sell_qty:
                            completed_sell_orders += 1
                            max_buy_order.order_qty = buy_qty - sell_qty
                            matched_qty = sell_qty
                        elif sell_qty == buy_qty:
                            self.buy_list.pop()
                            self.sell_list = self.sell_list[1:]
                            matched_qty = sell_qty
                            break_flag = True
                        else:
                            self.buy_list.pop()
                            sell_order.order_qty = sell_qty - buy_qty
                            matched_qty = buy_qty
                            break_flag = True
                        matched_queries.append(
                            "%s %s %s %s" % (sell_order.order_id,
                                             matched_qty,
                                             sell_order.stock_value,
                                             max_buy_order.order_id))
                    else:
                        break_flag = True
                    if break_flag:
                        break
                if completed_sell_orders:
                    self.sell_list = self.sell_list[completed_sell_orders:]
            else:
                min_sell_order = self.sell_list[0]
                completed_buy_orders = 0
                # for a new sell order, multiple queries from buy list are
                # matched as long as formula holds good
                for index in range(len(self.buy_list)-1, -1, -1):
                    break_flag = False
                    buy_order = self.buy_list[index]
                    sell_qty = min_sell_order.order_qty
                    if min_sell_order.stock_value <= buy_order.stock_value:
                        buy_qty = buy_order.order_qty
                        if buy_qty > sell_qty:
                            buy_order.order_qty = buy_qty - sell_qty
                            self.sell_list = self.sell_list[1:]
                            matched_qty = sell_qty
                            break_flag = True
                        elif buy_qty == sell_qty:
                            self.buy_list.pop()
                            self.sell_list = self.sell_list[1:]
                            matched_qty = sell_qty
                            break_flag = True
                        else:
                            completed_buy_orders -= 1
                            min_sell_order.order_qty = sell_qty - buy_qty
                            matched_qty = buy_qty
                        matched_queries.append(
                                "%s %s %s %s" % (min_sell_order.order_id,
                                                 matched_qty,
                                                 min_sell_order.stock_value,
                                                 buy_order.order_id))
                    else:
                        break_flag = True
                    if break_flag:
                            break
                if completed_buy_orders:
                    self.buy_list = self.buy_list[:completed_buy_orders]
