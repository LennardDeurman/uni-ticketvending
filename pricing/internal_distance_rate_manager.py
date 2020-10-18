from stations.station import Station
class InternalDistanceRateManager:

    RATES = {
		"UTR-C": {
			"GOU": 32,
			"GELD": 26,
			"HILV": 18,
			"DUIV": 31,
			"WEE": 33
		},
		"GOU": {
			"GELD": 58,
			"HILV": 50,
			"DUIV": 54,
			"WEE": 57
		},
		"GELD": {
			"HILV": 44,
            "DUIV": 57,
            "WEE": 59
		},
        "HILV": {
            "DUIV": 18,
            "WEE": 15
        }, 
        "DUIV": {
            "WEE": 3
        }
	}

    def __find_rate(self, from_station : Station, to_station : Station) -> float:
        try:
            return InternalDistanceRateManager.RATES[from_station.key][to_station.key]
        except:
            return 0.0

    def rate_between_stations(self, from_station : Station, to_station : Station) -> float:


        rate = self.__find_rate(
            from_station=from_station,
            to_station=to_station
        )

        reversed_rate = self.__find_rate(
            to_station=from_station,
            from_station=to_station
        )
        
    
        return max([rate, reversed_rate])