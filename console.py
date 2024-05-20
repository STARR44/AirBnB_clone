#!/usr/bin/python3
"""This module contains the entry point of the interpreter"""
import cmd
from models.base_model import BaseModel
from models.__init__ import storage


classes = {'BaseModel': BaseModel}

class HBNBCommand(cmd.Cmd):
    """This class represents an interpreter"""

    prompt = '(hbnb) '

    def do_create(self, arg):
        """Creates a new instance of a class"""
        if arg == "":
            print("*** class name missing ***")
        elif arg not in classes:
            print("** class doesn't exist **")
        else:
            obj = classes[arg]() # create the instance
            obj.save() #save instance
            print(obj.id)
    def do_quit(self, arg):
        """Exits the program"""
        return True

    def do_EOF(self, arg):
        """Exits the program when an EOF signal is received"""
        print()
        return True

    def emptyline(self):
        """Does nothing when line is empty"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
