from template.orders.lineitem import LineItem
from template.database_object import DatabaseObject
from typing import List

class Order(DatabaseObject):

    is_finished : bool
    line_items : List[LineItem]

    def __init__(self):
        self.line_items = List[LineItem]()
        self.is_finished = False

    def calculate_price(self):
        return sum(map(lambda x: x.calculate_price(), self.line_items))

