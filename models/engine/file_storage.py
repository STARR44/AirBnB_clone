#!/usr/bin/python3
"""This module defines the class FileStorage"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
}


class FileStorage:
    """This class serializes instances to a JSON file and vice versa"""

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""

        return FileStorage.__objects

    def new(self, obj):
        """Sets __objects

        Args:
        obj(object): instance of a class
        """
        
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""

        # convert the objects to their dict representation
        tmp = {}
        for key, value in FileStorage.__objects.items():
            tmp[key] = value.to_dict()

        with open(FileStorage.__file_path, 'w') as f:
            json.dump(tmp, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        from models.base_model import BaseModel

        try:
            tmp = {}
            with open(FileStorage.__file_path, 'r') as f:
                tmp = json.load(f)
            for key, value in tmp.items():
                FileStorage.__objects[key] = classes[value['__class__']](**value)

        except FileNotFoundError:
            pass # do nothing if file does not exist
