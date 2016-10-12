# stock_order_matching_sytem

An system that matches buy and sell orders based on price-time priority algorithm.

To run the program along with the test cases execute:
python main.py (stock_order_matching_sytem/ main.py)

# Sample input to test the program:

\#1 09:45 XAM sell 100 240.10<br/>
\#2 09:45 XAM sell 90 237.45<br/>
\#3 09:47 XAM buy 80 238.10<br/>
\#5 09:48 XAM sell 220 241.50<br/>
\#6 09:49 XAM buy 50 238.50<br/>
\#7 09:50 TCS buy 10 1001.10<br/>
\#8 10:01 XAM sell 20 240.10<br/>
\#9 10:02 XAM buy 150 242.70<br/>
\#10 10:5 TCS sell 5 1002<br/>
\#11 10:05 TCS buy 7 1003.10<br/>
\#12 10:06 TCS sell 5 1001<br/>

# Expected output of the program
<sell-order_id>  <sell/buy_qty> <stock_value_sold_at>  <buy_order_id>    
\#2 80 237.45 #3<br/>
\#2 10 237.45 #6<br/>
\#8 20 240.1 #9<br/>
\#1 100 240.1 #9<br/>
\#5 30 241.5 #9<br/>
\#10 5 1002.0 #11<br/>
\#12 2 1001.0 #11<br/>
\#12 3 1001.0 #7<br/>


