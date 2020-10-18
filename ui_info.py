from enum import IntEnum
from orders.enums import ClassType, DiscountRate


class UIWay(IntEnum):
	OneWay = 1
	Return = 2

class UIPayment(IntEnum):
	DebitCard = 1
	CreditCard = 2
	Cash= 3

class UIInfo:
	from_station: str = ""
	to_station: str = ""
	travel_class: ClassType = ClassType.SecondClass
	way: UIWay = UIWay.OneWay
	discount: DiscountRate = DiscountRate.NoDiscount
	payment: UIPayment

	def __init__(self, from_station: str, to_station: str, travel_class: ClassType, way: UIWay, discount: DiscountRate, payment: UIPayment):
		self.from_station = from_station
		self.to_station = to_station
		self.travel_class = travel_class
		self.way = way
		self.discount = discount
		self.payment = payment

	@property
	def is_retour(self):
		return self.way == UIWay.Return