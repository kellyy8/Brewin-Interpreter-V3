from intbase import InterpreterBase, ErrorType
from bparser import BParser
from ClassDefinitionv2 import ClassDefinition

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase’s constructor
        self.classes = {}

    # Map classes to their definitions.
    def __track_all_classes__(self, parsed_program):
        for class_def in parsed_program:
            if class_def[1] in self.classes:
                super().error(ErrorType.TYPE_ERROR, "Duplicate classes not allowed.")
            self.classes[class_def[1]] = class_def[2:]                                      # {'class_name' : ['class_def']}

    # Returns a list containing a particular class's definition.
    # TODO: Return something else if class_name is not a key (class does not exist) (where to handle it)
    def __find_class_definition__(self, class_name):
        return self.classes.get(class_name)                                                 # returns: ['class_def']
    
    def run(self, program):
        # parse the program into a more easily processed form
        result, parsed_program = BParser.parse(program)
        if result == False:
            return super().error(ErrorType.SYNTAX_ERROR, "Failed to parse file.")            #TODO: Check if this is the right ERROR_TYPE.
        else:
            # print(parsed_program)
            # print("-------------------------------------------------------------------------------------------------------------")
            self.__track_all_classes__(parsed_program)
            class_def = self.__find_class_definition__(super().MAIN_CLASS_DEF)
            # if class_def is None:
            #     super().error(ErrorType.SYNTAX_ERROR, "Must have a 'main' class.")

            # create a "main" class --> create object of type "main" --> call object's "main" method
            main_class = ClassDefinition(super().MAIN_CLASS_DEF, class_def, self)
            main_obj = main_class.instantiate_object()
            main_obj.call_main_method(super().MAIN_FUNC_DEF)


# class MethodDefinition:
#     # store all variables (accounts for shadowing...)
#     def __init__(self, method_def, object):
#         self.visible_variables = object.my_fields
#         self.method_def = method_def

#     def __add_variables(self, name, val):
#         self.visible_variables[name] = val

filename = "/Users/kellyyu/Downloads/23SP/CS131/Projects/spring-23-autograder/brew++.txt"
file_object = open(filename)
file_contents = []
for line in file_object:
    file_contents.append(line)
file_object.close()

inputStrings = ""
for item in file_contents:
    inputStrings += item

test = Interpreter()
test.run(file_contents)