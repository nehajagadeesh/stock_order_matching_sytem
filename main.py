from tests.run_tests import main as run_test_suite
from order_matching import OrderMatching


# runs the test suite and then executes the program
run_test_suite()
print "**********************End of test suite ******************************"
print "********************** Executing program ******************************"
order_matching_obj = OrderMatching()
order_matching_obj.main()