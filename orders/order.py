from orders.lineitem import LineItem
from payments.payment_operation import PaymentResponse
from database import DatabaseObject
from typing import List

class Order(DatabaseObject):

    is_finished : bool
    line_items : List[LineItem]
    payment_response : PaymentResponse

    def __init__(self):
        self.line_items = list()
        self.is_finished = False
        self.payment_response = None

    def calculate_price(self):
        return sum(list(map(lambda x: x.calculate_price(), self.line_items)))

