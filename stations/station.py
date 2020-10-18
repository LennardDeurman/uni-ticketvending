from database import DatabaseObject
class Station(DatabaseObject):

    name : str
    key : str

    def __init__(self, name : str, key : str):
        super().__init__()
        self.name = name
        self.key = key
 