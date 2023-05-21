from intbase import InterpreterBase, ErrorType
from bparser import BParser
from ObjectDefinitionv2 import ObjectDefinition

# INHERITANCE: ['class', 'class_name', 'inherits', 'parent_class_name', [field1], [field2], [method1], [method2]]
# no inheritance: ['class', 'class_name', [field1], [field2], [method1], [method2]]

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase’s constructor
        self.classes = {}
        self.caller = None

    def set_caller(self, caller):
        self.caller = caller

    def get_caller(self):
        return self.caller

    # Map classes to their definitions.
    def __track_all_classes__(self, parsed_program):
        for class_def in parsed_program:
            if class_def[1] in self.classes:
                super().error(ErrorType.TYPE_ERROR, "Duplicate classes not allowed.")
            else:
                # INHERITANCE
                if type(class_def[2]) != list:
                    self.classes[class_def[1]] = (class_def[3], class_def[4:])              # {'class_name' : ('parent_class_name', ['class_def'])}
                # no inheritance
                else:
                    self.classes[class_def[1]] = (None, class_def[2:])                      # {'class_name' : (None, ['class_def'])}

    # Returns a list containing a particular class's definition.
    # TODO: Return something else if class_name is not a key (class does not exist) (where to handle it)
    def __find_class_definition__(self, class_name):
        return self.classes.get(class_name)                                                 # returns: ( 'parent'/None, ['class_def'] )
    
    def run(self, program):
        # parse the program into a more easily processed form
        result, parsed_program = BParser.parse(program)
        if result == False:
            return super().error(ErrorType.SYNTAX_ERROR, "Failed to parse file.")            #TODO: Check if this is the right ERROR_TYPE.
        else:
            # print(parsed_program)
            # print("-------------------------------------------------------------------------------------------------------------")
            self.__track_all_classes__(parsed_program)
            class_def_tuple = self.__find_class_definition__(super().MAIN_CLASS_DEF)

            if class_def_tuple is None:
                super().error(ErrorType.TYPE_ERROR, "No class named 'main' found.")

            # NON INHERITANCE CHANGE!
            # create object of type "main" --> call object's "main" method
            main_obj = ObjectDefinition(self, super().MAIN_CLASS_DEF, class_def_tuple)
            main_obj.call_main_method(super().MAIN_FUNC_DEF)


# filename = "/Users/kellyyu/Downloads/23SP/CS131/Projects/spring-23-autograder/brew++.txt"
# file_object = open(filename)
# file_contents = []
# for line in file_object:
#     file_contents.append(line)
# file_object.close()

# inputStrings = ""
# for item in file_contents:
#     inputStrings += item

# test = Interpreter()
# test.run(file_contents)