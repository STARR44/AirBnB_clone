#!/usr/bin/python3
"""This module defines the baseModel class"""
import uuid
import datetime

class BaseModel:
    """This class define all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Initializes instance of class"""

        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at":
                elif key == "updated_at":
                    value = datetime.datetime.fromisoformat(value)
                elif key == "__class__":
                    pass
                else:
                    setattr(self, key, value)
        else:
                    self.id = str(uuid.uuid4())
                    self.created_at = datetime.datetime.now()
                    self.updated_at = datetime.datetime.now()
    def __str__(self):
        """return string representation of t object"""
        return f"[BaseModel]({self.id}) {self.__dict__}"

    def save(self):
        """updates <updated_at> with the current datetime"""
        updated_at = datetime.datetime.now()

    def to_dict(self):
        """returns a dictionary containing\
            all keys/values of __dict__ of the instance"""
        self.__dict__['__class__'] = 'BaseModel'
        self.__dict__['created_at'] = self.created_at.isoformat()
        self.__dict__['updated_at'] = self.updated_at.isoformat()
        return self.__dict__
