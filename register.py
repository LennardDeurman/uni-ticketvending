from datetime import datetime
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Register(Generic[T]):

	def find_all(self) -> List[T]:
		return self.database.find_all()
		
	def commit(self, objects: List[T]):
		self.database.schedule_objects(objects)
		self.database.write()
	
	def find_by_id(self, sid: int):
		return self.database.first_where(
			{
				"sid": sid
			}
		)
