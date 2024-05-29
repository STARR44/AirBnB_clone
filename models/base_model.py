#!/usr/bin/python3
"""This module defines the baseModel class"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """This class defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Initializes instance of class"""

        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)  # Set __objects if instance is new
        else:
            for key, value in kwargs.items():
                if key not in ('created_at', 'updated_at', '__class__'):
                    setattr(self, key, value)
            self.created_at = datetime.fromisoformat(kwargs.get('created_at'))
            self.updated_at = datetime.fromisoformat(kwargs.get('updated_at'))

    def __str__(self):
        """return string representation of t object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates <updated_at> with the current datetime"""

        self.updated_at = datetime.now()
        models.storage.save()  # Serialize data to JSON file

    def to_dict(self):
        """returns a dictionary containing\
            all keys/values of __dict__ of the instance"""

        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict
