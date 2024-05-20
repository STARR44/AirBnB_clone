#!/usr/bin/python3
"""This module defines the class FileStorage"""
import json


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
        
        obj_dict = obj.to_dict()
        key = f"{obj_dict['__class__']}.{obj.id}"
        FileStorage.__objects[key] = obj_dict

    def save(self):
        """Serializes __objects to the JSON file"""

        with open(FileStorage.__file_path, 'w') as f:
            json.dump(FileStorage.__objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""

        try:
            with open(FileStorage.__file_path, 'r') as f:
                FileStorage.__objects = json.load(f)
        except FileNotFoundError:
            pass # do nothing if file does not exist
