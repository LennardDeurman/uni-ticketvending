from datetime import datetime
from typing import TypeVar, Generic, List

T = TypeVar('T')

class DatabaseObject:

	def __init__(self):
		self.sid = None
		self.date_created = datetime.now()
		self.is_modified = False

	def parse(self, dictionary:dict): #Used for updating TODO: to be implemented 
		pass
	
	def to_dict(self): #Used for saving and updating existing objects
		return {}


class Database(Generic[T]):

	def __init__(self):
		self.__saved_objects = list()
		self.__scheduled_objects = list()


	def schedule_objects(self, objects : List[T]):
		self.__scheduled_objects += objects

	def first_where(self, query : dict) -> T:
		found_objects = self.where(
			query=query
		)
		if (len(found_objects) > 0):
			return found_objects[0]
		return None

	def where(self, query : dict) -> List[T]:
		found_objects = list()
		for saved_object in self.__saved_objects:
			valid = False
			for key in query.keys():
				if (getattr(saved_object, key) == query[key]):
					valid = True
			if valid:
				found_objects.append(saved_object)
		return found_objects
	
	def find_all(self) -> List[T]:
		return self.__saved_objects

	def write(self):
		items_to_process = self.__scheduled_objects.copy()
		for scheduled_object in self.__scheduled_objects:
			existing_object = self.first_where({
				"sid": scheduled_object.sid
			})
			if existing_object != None:
				existing_object.parse(scheduled_object.dict())
				items_to_process.remove(scheduled_object)
 
		self.__saved_objects += items_to_process
		self.__scheduled_objects = list()