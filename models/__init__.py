#!/usr/bin/python3
"""Creates an instance of FileStorage when models is imported"""
from .engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()  # Load data stored JSON file
