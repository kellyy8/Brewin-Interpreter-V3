from intbase import InterpreterBase
from bparser import BParser

filename = "/Users/kellyyu/Downloads/23SP/CS131/P1/spring-23-project-starter/brew.txt"
file_object = open(filename)
file_contents = []
for line in file_object:
    file_contents.append(line)
file_object.close()

inputStrings = ""
for item in file_contents:
    inputStrings += item

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase’s constructor

    def run(self, program):
        # parse the program into a more easily processed form
        result, parsed_program = BParser.parse(program)
        if result == False:
            return super().error(3, "Failed to parse file.")
        else:
            self.__track_classes__(parsed_program)

    # map classes to their definitions
    def __track_classes__(self, parsed_program):
        self.classes = {}
        for class_def in parsed_program:
            self.classes[class_def[1]] = class_def[2:]                  # {'class_name' : ['class_def']}

    # returns a list containing a particular class's definition
    def __find_class_definition__(self, class_name):
        return self.classes[class_name]                                 # returns: ['class_def']
    
# FIX: run method "main", using run_statement for testing purposes
    def run_main_method(self):
        class_def = self.__find_class_definition__("main")
        main_class = ClassDefinition("main", class_def)
        main_obj = main_class.instantiate_object()
        main_obj.run_statement(['print', '"hello world!"'])

"""     √ self.__discover_all_classes_and_track_them(parsed_program)
        √ class_def = self.__find_definition_for_class("main")
        √ obj = class_def.instantiate_object()  # function for classes -- to create instances of class type
        obj.run_method("main")  # function -- to run methods associated with objects
"""
   # for class_def in parsed_program:
        #     for item in class_def:
        #         if item[0] == 'field':
        #             # handle a field
        #             print(item[0])
        #         elif item[0] == 'method':
        #             # handle a method
        #             print(item[0])
 # def interpret_statement(self, line_number, statement):

class ClassDefinition:
    # constructor for a ClassDefinition
    def __init__(self, name, definition):
        # store name of each class & their methods (list) and fields (list)
        self.class_name = name
        self.my_methods = []
        self.my_fields = []

        for item in definition:
            if item[0] == 'field':
                self.my_fields.append(item)       #['field', 'field_name', 'init_value']
            elif item[0] == 'method':
                self.my_methods.append(item)      #['method', 'method_name', ['params'], ['top-level statement' [body or sub-methods]]]

    # uses the definition of a class to create and return an instance of it (assemble object)
    def instantiate_object(self): 
        # create an instance
        obj = ObjectDefinition()
        for method in self.my_methods:
            obj.add_method(method[1], method[2:])
        for field in self.my_fields:
            obj.add_field(field[1], field[2])
        return obj     

# ex: print_statement = ['print', '"hello world!"']
# pass in args of print statement expression
def execute_print_statement(statement):
    itp = Interpreter()
    for arg in statement:
        # string arg
        if arg[0] == '"' and arg[-1] == '"':
            itp.output(arg[1:-1])
# print_statement = ['"hello world!"']
# execute_print_statement(print_statement)

class ObjectDefinition:
    def __init__(self):
        self.my_methods = {}
        self.my_fields = {}

    # map 'method' to its 'definition'
    def add_method(self, method_name, method_def):
        self.my_methods[method_name] = method_def       #{'method_name' : ['params'], ['top-level statement' [body or sub-methods]]}
    
    # map 'field' to its 'initial value'
    def add_field(self, name, init_val):
        self.my_fields[name] = init_val                 #{'field_name' : 'init_value' (can hold curr value later too)}

# IMPLEMENT
    # Interpret the specified method using the provided parameters    
    def call_method(self, method_name, parameters):
        """ method = self.__find_method(method_name)
        statement = method.get_top_level_statement()
        result = self.__run_statement(statement)
        return result """
        method = self.__find_method(method_name)
        statement = self.get_top_level_statement(method_name)
        result = self.__run_statement(statement)
        return result

# IMPLEMENT, understand logic :(

    # find method's definition by method name
    def __find_method(self, method_name):
        return self.my_methods[method_name]
    
    # get top level statement (single line or 'begin' with sublines)
    def get_top_level_statement(self, method_name):
        return self.my_methods[method_name][3][0]

    # runs/interprets the passed-in statement until completion and gets the result, if any
    def run_statement(self, statement):
        if False:
            return 0
        if statement[0] == 'print':
            result = execute_print_statement(statement)
        # elif is_an_input_statement(statement):
        #     result = self.__execute_input_statement(statement)
        # elif is_a_call_statement(statement):
        #     result = self.__execute_call_statement(statement)
        # elif is_a_while_statement(statement):
        #     result = self.__execute_while_statement(statement)
        # elif is_an_if_statement(statement):
        #     result = self.__execute_if_statement(statement)
        # elif is_a_return_statement(statement):
        #     result = self.__execute_return_statement(statement)
        # elif statement == 'begin':
        #     result = self.__execute_all_sub_statements_of_begin_statement(statement) 
        return result
        # return 0

test = Interpreter()
test.run(file_contents)
test.run_main_method()
# main = test.__find_class_definition__("main")
# print(main)



