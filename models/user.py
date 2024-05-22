#!/usr/bin/python3
"""This module contains the class user"""
from models.base_model import BaseModel


class User(BaseModel):
    """This class represents a user"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

