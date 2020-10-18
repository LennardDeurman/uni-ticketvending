from database import Database
from register import Register
from orders.order import Order
from payments.payment_operation import PaymentResponse

class OrderDatabase(Database[Order]):
	pass

class OrderRegister(Register[Order]):
	
	def __init__(self):
		self.database = OrderDatabase()

	def create_new(self, line_items = []) -> Order:
		order = Order()
		order.line_items = line_items
		return order

	def finish(self, order: Order, payment_response : PaymentResponse):
		order.is_finished = True
		order.payment_response = payment_response
		order.is_modified = True
		self.commit([order])
