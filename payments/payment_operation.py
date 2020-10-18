from datetime import datetime
from payments.creditcard import CreditCard
from payments.debitcard import DebitCard
from payments.coin_machine import IKEAMyntAtare2000

class PaymentResponse:
	
	def __init__(self, total_price):
		self.total_price = total_price
		self.date_created = datetime.now()


class PaymentOperation:

	price : int

	CREDIT_CARD_FEE = 0.50

	def __init__(self, price):
		self.price = price

	def pay_with_creditcard(self):
		c = CreditCard()
		c.connect()
		total_price = self.price + PaymentOperation.CREDIT_CARD_FEE
		ccid: int = c.begin_transaction(round(total_price, 2))
		c.end_transaction(ccid)
		c.disconnect()
		return PaymentResponse(total_price) 

	def pay_with_debitcard(self):
		d = DebitCard()
		d.connect()
		dcid: int = d.begin_transaction(round(self.price, 2))
		d.end_transaction(dcid)
		d.disconnect()
		return PaymentResponse(self.price)

	def pay_by_cash(self):
		coin = IKEAMyntAtare2000()
		coin.starta()
		coin.betala(int(round(self.price * 100)))
		coin.stoppa()
		return PaymentResponse(self.price)
