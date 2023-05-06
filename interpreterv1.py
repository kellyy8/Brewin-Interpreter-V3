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

test_statement =['print', '1', '"here\'s a result "', ['*', '3', '5'], '" and here\'s a boolean"', 'true', '" "', ['+', '"race"', '"car"']]

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase’s constructor

     # map classes to their definitions
    def __track_classes__(self, parsed_program):
        self.classes = {}
        for class_def in parsed_program:
            self.classes[class_def[1]] = class_def[2:]                  # {'class_name' : ['class_def']}

    # returns a list containing a particular class's definition
    def __find_class_definition__(self, class_name):
        return self.classes[class_name]                                 # returns: ['class_def']
    
    def run(self, program):
        # parse the program into a more easily processed form
        result, parsed_program = BParser.parse(program)
        if result == False:
            return super().error(3, "Failed to parse file.")
        else:
            print(parsed_program)
            self.__track_classes__(parsed_program)
            class_def = self.__find_class_definition__("main")
            main_class = ClassDefinition("main", class_def)
            main_obj = main_class.instantiate_object()
            # for item in test_statement:
            #     main_obj.run_statement(item)     # FIX: run method "main", using run_statement for testing purposes
            main_obj.run_statement(test_statement)

"""     √ self.__discover_all_classes_and_track_them(parsed_program)
        √ class_def = self.__find_definition_for_class("main")
        √ obj = class_def.instantiate_object()  # function for classes -- to create instances of class type
        obj.run_method("main")  # function -- to run methods associated with objects
"""

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

def  evaluate_expression(expression):    #returns int, string, bool, or object reference
    itp = Interpreter()
    # expr examples = ['>', 'n', '0'], ['*', 'n', 'result'], ['call', 'me', 'factorial', 'num']
    add_op = {'+'}
    math_ops = {'-', '*', '/', '%'}
    only_int_and_str_compare_ops = {'<', '>', '<=', '>='}
    only_bool_compare_ops = {'&', '|'}
    any_compare_ops = {'==', '!='}
    compare_ops = only_int_and_str_compare_ops.union(only_bool_compare_ops.union(any_compare_ops))
    
    # new code
    stack = []
    all_ops = add_op.union(math_ops.union(compare_ops))
    
    for expr in reversed(expression):
        # TODO: Handle unary NOT operation.
        # TODO: Handle function calls & object instantiations (may return string, int, bool, or object?)
        #     elif expr[0] == 'call':
        #         itp.output("Call function.")
        #     elif expr[0] == 'new':
        #         itp.output("Instantiate new object.")

        # 'expression' operand
        if type(expr) == list:
            stack.append(expr)

        elif expr == '!':
            op = stack.pop()
            if op!='true' and op!='false':
                itp.error(1, "Unary operations only works with boolean operands.")
            elif op=='true':
                stack.append('false')
            else:
                stack.append('true')

        elif expr in all_ops:
            op1 = stack.pop()
            op2 = stack.pop()

            # set up operand for nested expressions: returned value of function, variable, or constant
            if type(op1) == list:
                op1 = evaluate_expression(op1)
            # TODO: Get value from existing variables (parameters or fields).
            # otherwise, op1 is a constant

            if type(op2) == list:
                op2 = evaluate_expression(op2)
            # TODO: Get value from existing variables (parameters or fields).
            # otherwise, op2 is a constant

            # TODO: Account for op1 and op2 being objects. (not sure if i need to do this; it's for null vs objects)
            # convert op1 and op2 into int, string, or bool constants, or null
            if op1[0] == '"': op1 = op1[1:-1]
            elif op1 == 'true': op1 = True
            elif op1 == 'false': op1 = False
            elif op1 == 'null': op1 = None
            else: op1 = int(op1)

            if op2[0] == '"': op2 = op2[1:-1]
            elif op2 == 'true': op2 = True
            elif op2 == 'false': op2 = False
            elif op2 == 'null': op2 = None
            else: op2 = int(op2)

            # check for type compatibility & operand compatibility
            if expr=='+' and not(type(op1)==int and type(op2)== int) and not(type(op1)==str and type(op2)==str):
                itp.error(1, "'+' only works with integers and strings.")
            elif expr in math_ops and (type(op1) != int or type(op2) != int):
                itp.error(1, "Math operations only compatible with integers.")
            elif expr in compare_ops:
                if (expr in only_bool_compare_ops):
                    if not (type(op1)==bool and type(op2)==bool):
                        itp.error(1, "Logical AND and OR operations only compatible with booleans.")
                elif (expr in only_int_and_str_compare_ops):
                    if not(type(op1)==int and type(op2)==int) and not(type(op1)==str and type(op2)==str):
                        itp.error(1, "Operands must both be integers or strings.")
                else:
                    if op1!=None and op2!=None and not(type(op1)==int and type(op2)==int) and not(type(op1)==str and type(op2)==str) and not(type(op1)==bool and type(op2)==bool):
                        itp.error(1, "Operands must match for '==' or '!='.")

            # perform math or compare operation:
            match expr:
                # returns string or integer values
                case '+': result = op1 + op2
                # returns integer values
                case '-': result = op1 - op2
                case '*': result = op1 * op2
                case '/': result = op1 // op2
                case '%': result = op1 % op2
                # returns boolean values
                case '>': result = op1 > op2
                case '<': result = op1 < op2
                case '>=': result = op1 >= op2
                case '<=': result = op1 <= op2
                case '==': result = op1 == op2
                case '!=': result = op1 != op2
                case '&': result = op1 & op2              #TODO: check if this a correct translation lol
                case '|': result = op1 | op2

            # reformat to the way ints, bools, and strings are represented
            if(type(result)==int):
                result = str(result)
            elif(type(result)==str):
                result = '"' + result + '"'
            elif(type(result)==bool):
                if(result): result = 'true'
                else: result = 'false'

            stack.append(result)

        else:
            stack.append(expr)
        
    return stack.pop()

    # new code

def execute_print_statement(statement):     #not printing object refs or null
    output = ""
    for arg in statement:
        # expressions evaluating to str, int, bool values
        if type(arg) == list:
            result = evaluate_expression(arg)
            # remove "" from Brewin strings
            if(result[0]=='"'):
                result = result[1:-1]
            output += result
        
        # string constants
        elif arg[0] == '"':
            output += arg[1:-1]
        
        # TODO: vars referring to str, int, bool values (check if it's a field or parameter var)
        # default case: integer and boolean constants --> printed out as they are passed into the print method
        else:
            output += arg
    
    itp = Interpreter()
    itp.output(output)

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
            result = execute_print_statement(statement[1:])
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
