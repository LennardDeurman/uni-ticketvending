from database import Database
from register import Register
from stations.station import Station

class StationDatabase(Database[Station]):
	


	dummy_objects = [ 
            Station(
                name="Utrecht Centraal",
                key="UTR-C"
            ),
            Station(
                name="Gouda",
                key="GOU"
            ),
            Station(
                name="Geldermalsen",
                key="GELD"
            ),
            Station(
                name="Hilversum",
                key="HILV"
            ),
            Station(
                name="Duivendrecht",
                key="DUIV"
            ),
            Station(
                name="Weesp",
                key="WEE" 
            )
        ]

	def __init_dummies(self):
		self.schedule_objects(self.dummy_objects)
		self.write()

	def __init__(self):
		self.__init_dummies()
		
    

class StationRegister(Register[Station]):
	
	def __init__(self):
		self.database = StationDatabase()

	def find_by_name(self, name : str) -> Station:
		return self.database.first_where(
			{
				"name": name
			}
		)
	
	def find_by_key(self, key : str) -> Station:
		return self.database.first_where(
			{
				"key": key
			}
		)