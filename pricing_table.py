class PricingTable:

    BaseRateMapping = {
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
    def get_price(tariefeenheden: int, col: int) -> float:
        price = 0
        price = price * 0.02 * tariefeenheden
        return round(price, 2)
