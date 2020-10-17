from abc import ABC, abstractmethod
from datetime import datetime
from enum import IntEnum
from typing import List

class InternalDistanceRateManager:

    def __init__(self):
        pass

    def rate_between_stations(from_station : Station, to_station : Station):
        pass
    

class PricingManager:

    BASE_RATE_MAPPING = {
        ClassType.FirstClass: {
            DiscountRate.NoDiscount: 3.60,
            DiscountRate.TwentyDiscount: 2.90,
            DiscountRate.FortyDiscount: 2.20
        },
        ClassType.SecondClass: {
            DiscountRate.NoDiscount: 2.10,
            DiscountRate.TwentyDiscount: 1.70,
            DiscountRate.FortyDiscount: 1.30
        }
    }


    @staticmethod
    def __find_base_rate(class_type : ClassType, discount_rate : DiscountRate):
        try:
            return PricingManager.BASE_RATE_MAPPING[class_type][discount_rate]
        except:
            raise Exception("Base rate for this class type and discount rate combination is not present in the mapping")

    @staticmethod
    def calculate_price(from_station : Station, to_station: Station, discount_rate : DiscountRate, class_type : ClassType, is_retour) -> float:
        base_rate = PricingManager.__find_base_rate(class_type, discount_rate)
        distance_rate = InternalDistanceRateManager().rate_between_stations(from_station, to_station)
        price = base_rate * 0.02 * distance_rate
        price = round(price, 2)
        if is_retour:
            price = price * 2
        return price


class ClassType(IntEnum):
    FirstClass = 1,
    SecondClass = 2

class DiscountRate(IntEnum):
	NoDiscount = 1
	TwentyDiscount = 2
	FortyDiscount = 3

class DatabaseObject:

    sid : int
    date_created : datetime 
    is_modified : bool

class Station(DatabaseObject):

    name : str

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

class Order(DatabaseObject):

    is_finished : bool
    line_items : List[LineItem]

    def __init__(self):
        self.line_items = List[LineItem]()
        self.is_finished = False

    def calculate_price(self):
        return sum(map(lambda x: x.calculate_price(), self.line_items))



    
