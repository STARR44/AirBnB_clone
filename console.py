#!/usr/bin/python3
"""This module contains the entry point of the interpreter"""
import cmd
from models.base_model import BaseModel
from models.__init__ import storage

classes = {'BaseModel': BaseModel}
objects = storage.all()


class HBNBCommand(cmd.Cmd):
    """This class represents an interpreter"""

    prompt = '(hbnb) '

    def do_all(self, arg):
        """Prints all string representation of all instances"""

        obj_list = []
        if not arg:
            for key, value in objects.items():
                class_name = key.split('.')[0]
                obj = classes[class_name](**value)  # recreates obj
                obj_list.append(str(obj))
            print(obj_list)
        elif arg and arg not in classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                class_name = key.split('.')[0]
                if class_name == arg:
                    obj = classes[arg](**value) 
                    obj_list.append(str(obj))
            print(obj_list)
            
    def do_create(self, arg):
        """Creates a new instance of a class"""

        if arg == "":
            print("*** class name missing ***")
        elif arg not in classes:
            print("** class doesn't exist **")
        else:
            obj = classes[arg]()  # create the instance
            obj.save()  # save instance
            print(obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""

        args = arg.split()
        if arg == "":
            print("*** class name missing ***")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            # Get dict representation of obj
            key = f"{args[0]}.{args[1]}"
            try:
                obj_dict = objects[key]

                # Recreate obj
                obj = classes[args[0]](**obj_dict)

                print(obj)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on class name and id"""

        args = arg.split()
        if arg == "":
            print("*** class name missing ***")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            try:
                objects.pop(key)  # delete key
                storage.save()  # save changes
            except KeyError:
               print("** no instance found **")

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
