#!/usr/bin/python3
"""This module contains the entry point of the interpreter"""
import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import models

classes = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
}
objects = models.storage.all()


def parse(line):
    """Parse the line of arguments"""

    pattern = r'"[^"]*"|{.*}|\'[^\']*\'|[^\s]+'
    match = re.findall(pattern, line)

    return [e.strip("'\"") for e in match]


class HBNBCommand(cmd.Cmd):
    """This class represents an interpreter"""

    prompt = '(hbnb) '

    def default(self, arg):
        """default action if command is not found"""

        globals = {
                    'all': self.do_all,
                    'count': self.count,
                    'destroy': self.do_destroy,
                    'show': self.do_show,
                    'update': self.do_update,
                    'arguments': "" 
        }

        # parse line
        pattern = r'(?P<class_name>\w+)\.(?P<cmd>\w+)\((?P<args>.*)\)'
        match = re.match(pattern, arg)
        if match:
            class_name = match.group('class_name')
            cmd = match.group('cmd')
            args = match.group('args')
        else:
            print(f"** syntax error: {arg} **")
            return

        args_list = re.findall(r'".*?"|{.*}|[^,\s]+', args)
        print(args_list)

        uid = ""
        arg_1 = ""
        arg_2 = ""
        try:
            uid = args_list[0]
            arg_1 = args_list[1]
            arg_2 = args_list[2]
        except IndexError:
            pass
       
 
        globals['arguments'] = (f"{class_name} {uid} {arg_1} {arg_2}").strip()
        line = f"{cmd}(arguments)"
        print("Arguments:", globals['arguments'])
        eval(line, globals)

    def do_all(self, arg):
        """Prints all string representation of all instances"""

        obj_list = []
        args = parse(arg)
        if not args:
            for key, value in objects.items():
                obj_list.append(str(value))
            print(obj_list)
        elif args and args[0] not in classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                class_name = key.split('.')[0]
                if class_name == args[0]:
                    obj_list.append(str(value))
            print(obj_list)

    def do_create(self, arg):
        """Creates a new instance of a class"""

        if arg == "":
            print("** class name missing **")
        elif arg not in classes:
            print("** class doesn't exist **")
        else:
            obj = classes[arg]()  # create the instance
            obj.save()  # save instance
            print(obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""

        args = parse(arg)
        if arg == "":
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            # Get dict representation of obj
            key = f"{args[0]}.{args[1]}"
            try:
                obj = objects[key]
                print(obj)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on class name and id"""

        args = parse(arg)
        if arg == "":
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            try:
                objects.pop(key)  # delete key
                models.storage.save()  # save changes
            except KeyError:
               print("** no instance found **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""

        args = parse(arg)
        if not arg:
            print("** class name missing **")

        elif args[0] not in classes:
            print("** class doesn't exist **")

        elif len(args) == 1:
            print("** instance id missing **")

        else:
            key = f"{args[0]}.{args[1]}"
            try:
                obj = objects[key]

                if len(args) == 2:
                    print("** attribute name missing **")

                else:
                    try:
                        if type(eval(args[2])) == dict:
                            for attr_name, attr_value in eval(args[2]).items():
                                if attr_name in obj.__dict__:
                                    attr_type = type(obj.__dict__[attr_name])
                                    setattr(obj, attr_name, attr_type(attr_value))
                                else:
                                    setattr(obj, attr_name, attr_value)
                                obj.save()

                    except NameError:
                        if len(args) == 3:
                            print("** value missing **")

                        else:
                            attr_name = args[2]
                            attr_value = args[3]

                            if attr_name in obj.__dict__:
                                attr_type = type(obj.__dict__[attr_name])
                                setattr(obj, attr_name, attr_type(attr_value))

                            else:
                                setattr(obj, attr_name, attr_value)
                            obj.save()

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

    def count(self, class_name):
        """Counts all the instances of a class"""

        count = 0
        if class_name in classes:
            for key, value in objects.items():
                if class_name == key.split('.')[0]:
                    count += 1

            print(count)

        else:
            print("** class doesn't exist **")
        

if __name__ == '__main__':
    HBNBCommand().cmdloop()
