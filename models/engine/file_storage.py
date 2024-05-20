#!/usr/bin/python3
"""This module defines the class FileStorage"""
import json


class FileStorage:
    """This class serializes instances to a JSON file and vice versa"""

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""

        return __objects

    def new(self, obj):
        """Sets __objects

        Args:
        obj(object): instance of a class
        """
        
        obj_dict = obj.to_dict()
        key = f"{obj_dict['__class__']}.{obj.id}"
        __objects[key] = obj_dict

    def save(self):
        """Serializes __objects to the JSON file"""

        with open(__file_path, 'w') as f:
            json.dump(__objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""

        try:
            with open(__file_path, 'r') as f:
                __objects = json.load(f)
        except FileNotFoundError:
            pass # do nothing if file does not exist
