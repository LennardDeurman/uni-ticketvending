from template.pricing.internal_distance_rate_manager import InternalDistanceRateManager
from template.stations.station import Station
from template.orders.enums import DiscountRate, ClassType

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
 