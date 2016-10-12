# stock_order_matching_sytem

An system that matches buy and sell orders based on price-time priority algorithm.

To run the program along with the test cases execute:
python main.py (stock_order_matching_sytem/ main.py)

# Sample input to test the program:

\#1 09:45 XAM sell 100 240.10
\#2 09:45 XAM sell 90 237.45
\#3 09:47 XAM buy 80 238.10
\#5 09:48 XAM sell 220 241.50
\#6 09:49 XAM buy 50 238.50
\#7 09:50 TCS buy 10 1001.10
\#8 10:01 XAM sell 20 240.10
\#9 10:02 XAM buy 150 242.70
\#10 10:5 TCS sell 5 1002
\#11 10:05 TCS buy 7 1003.10
\#12 10:06 TCS sell 5 1001

# Expected output of the program
<sell-order_id>  <sell/buy_qty> <stock_value_sold_at>  <buy_order_id>    
\#2 80 237.45 #3
\#2 10 237.45 #6
\#8 20 240.1 #9
\#1 100 240.1 #9
\#5 30 241.5 #9
\#10 5 1002.0 #11
\#12 2 1001.0 #11
\#12 3 1001.0 #7


