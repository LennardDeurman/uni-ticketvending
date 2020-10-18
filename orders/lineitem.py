
from abc import ABC, abstractmethod
from datetime import datetime
from pricing.pricing_manager import PricingManager
from stations.station import Station
from orders.enums import DiscountRate, ClassType 


class Specification:
    
    @abstractmethod
    def calculate_price(self) -> float:
        pass


class TicketSpecification(Specification):
    validity_date : datetime
    is_retour : bool
    arrival : Station
    departure : Station
    class_type : ClassType
    discount : DiscountRate

    def __init__(self, validity_date : datetime, is_retour : bool, arrival : Station, departure : Station, discount : DiscountRate, class_type : ClassType):
        self.validity_date = validity_date
        self.is_retour = is_retour
        self.arrival = arrival
        self.departure = departure
        self.discount = discount
        self.class_type = class_type

    def calculate_price(self) -> float:
        return PricingManager().calculate_price(
            self.departure,
            self.arrival, 
            self.discount, 
            self.class_type,
            self.is_retour
        )

class LineItem:
    specification : Specification
    quantity : int

    def __init__(self, specification : Specification, quantity : int):
        self.specification = specification
        self.quantity = quantity

    def calculate_price(self) -> float:
        return self.quantity * self.specification.calculate_price()