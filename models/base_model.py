#!/usr/bin/python3
"""This module defines the baseModel class"""
import uuid
import datetime
from .__init__ import storage


class BaseModel:
    """This class defines all common attributes/methods for other classes"""

    def __init__(self):
        """Initializes instance of class"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        storage.new() # Set __objects if instance is new

    def __str__(self):
        """return string representation of t object"""
        return f"[BaseModel]({self.id}) {self.__dict__}"

    def save(self):
        """updates <updated_at> with the current datetime"""
        updated_at = datetime.datetime.now()
        storage.save() # Serialize data to JSON file

    def to_dict(self):
        """returns a dictionary containing\
            all keys/values of __dict__ of the instance"""
        self.__dict__['__class__'] = 'BaseModel'
        self.__dict__['created_at'] = self.created_at.isoformat()
        self.__dict__['updated_at'] = self.updated_at.isoformat()
        return self.__dict__
