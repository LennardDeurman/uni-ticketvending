
from abc import ABC, abstractmethod
from datetime import datetime
from template.pricing.pricing_manager import PricingManager
from template.stations.station import Station
from template.orders.enums import DiscountRate, ClassType 


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

    def __init__(self, validity_date : datetime, is_retour : bool, arrival : Station, departure : Station, discount : DiscountRate):
        self.validity_date = validity_date
        self.is_retour = is_retour
        self.arrival = arrival
        self.departure = departure
        self.discount = discount

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