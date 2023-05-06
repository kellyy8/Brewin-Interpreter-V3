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

test_statement = ['if', ['!=', '"a"', '"b"'], ['if', ['==', '1', '1'], ['print', '"nested if in if-body"']], ['if', ['==', '1', '1'], ['print', '"nested if in else-body"']]]

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
            print("-------------")
            self.__track_classes__(parsed_program)
            class_def = self.__find_class_definition__("main")
            main_class = ClassDefinition("main", class_def)
            main_obj = main_class.instantiate_object()
            # TODO: Run method "main". Currently using run_statement for testing.
            # for item in test_statement:
            #     main_obj.run_statement(item)
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

def  evaluate_expression(expression):    #return int/string ('""')/bool constants as strings, or an object reference
    # expr examples = ['true'] ['num'] ['>', 'n', '0'], ['*', 'n', 'result'], ['call', 'me', 'factorial', 'num']
    itp = Interpreter()

    if(type(expression)!=list):
        # TODO: if expression is a variable ==> retrieve and return its value
        # else expression is a constant ==> return expression
        return expression

    # expression is arithmetics, concatenation, or comparison (parameter is a list)
    add_op = {'+'}
    math_ops = {'-', '*', '/', '%'}
    only_int_and_str_compare_ops = {'<', '>', '<=', '>='}
    only_bool_compare_ops = {'&', '|'}
    any_compare_ops = {'==', '!='}
    compare_ops = only_int_and_str_compare_ops.union(only_bool_compare_ops.union(any_compare_ops))
    
    stack = []
    all_ops = add_op.union(math_ops.union(compare_ops))
    
    for expr in reversed(expression):
        # TODO: Handle function calls & object instantiations (may return string, int, bool, or object?)
        #     elif expr[0] == 'call':
        #         itp.output("Call function.")
        #     elif expr[0] == 'new':
        #         itp.output("Instantiate new object.")

        # 'expression' operand
        if type(expr)==list:
            stack.append(expr)
        # 'unary NOT' operand
        elif expr == '!':
            op = stack.pop()
            if op!=itp.TRUE_DEF and op!=itp.FALSE_DEF:
                itp.error(1, "Unary operations only works with boolean operands.")
            elif op==itp.TRUE_DEF:
                stack.append(itp.FALSE_DEF)
            else:
                stack.append(itp.TRUE_DEF)
        # perform operation
        elif expr in all_ops:
            op1 = stack.pop()
            op2 = stack.pop()

            # set up operand for nested expressions: returned value of function, variable, or constant
            if type(op1)==list:
                op1 = evaluate_expression(op1)
            # TODO: Get value from existing variables (parameters or fields).
            # otherwise, op1 is a constant

            if type(op2)==list:
                op2 = evaluate_expression(op2)
            # TODO: Get value from existing variables (parameters or fields).
            # otherwise, op2 is a constant

            # TODO: Account for op1 and op2 being objects. (not sure if i need to do this; it's for null vs objects)
            # convert op1 and op2 into int, string, or bool constants, or null
            if op1[0] == '"': op1 = op1[1:-1]
            elif op1 == itp.TRUE_DEF: op1 = True
            elif op1 == itp.FALSE_DEF: op1 = False
            elif op1 == itp.NULL_DEF: op1 = None
            else: op1 = int(op1)

            if op2[0] == '"': op2 = op2[1:-1]
            elif op2 == itp.TRUE_DEF: op2 = True
            elif op2 == itp.FALSE_DEF: op2 = False
            elif op2 == itp.NULL_DEF: op2 = None
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
                if(result): result = itp.TRUE_DEF
                else: result = itp.FALSE_DEF

            stack.append(result)

        # store operand into stack
        else:
            stack.append(expr)
        
    return stack.pop()

def execute_print_statement(statement):     #not printing object refs or null
    output = ""
    for arg in statement:
        # expressions evaluating to str, int, bool values
        if type(arg)==list:
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
    # TODO: Change all to private member functions later. Currently implementing some as public methods.
    def run_statement(self, statement):
        itp = Interpreter()
        result = "Did not succeeed :(."

        if statement[0] == itp.PRINT_DEF:
            result = execute_print_statement(statement[1:])
        # elif is_an_input_statement(statement):
        #     result = self.__execute_input_statement(statement)
        # elif is_a_call_statement(statement):
        #     result = self.__execute_call_statement(statement)
        # elif is_a_while_statement(statement):
        #     result = self.__execute_while_statement(statement)
        # elif is_a_return_statement(statement):
        #     result = self.__execute_return_statement(statement)
        elif statement[0] == itp.BEGIN_DEF:
            result = self.__execute_all_sub_statements_of_begin_statement(statement[1:])
        elif statement[0] == itp.IF_DEF:
            result = self.__execute_if_statement(statement[1:])
        return result

    def __execute_all_sub_statements_of_begin_statement(self, statement):
        for substatement in statement:
            self.run_statement(substatement)
    
    def __execute_if_statement(self, statement):            # [if, [[condition], [if-body], [else-body]]]
        itp = Interpreter()
        condition_result = evaluate_expression(statement[0])
        if_body = statement[1]

        # condition is not a boolean
        if(condition_result != itp.TRUE_DEF and condition_result != itp.FALSE_DEF):
            itp = Interpreter()
            itp.error(1, "Condition of the if statement must evaluate to a boolean type.")
        # condition passes
        elif(condition_result == itp.TRUE_DEF):
            self.run_statement(if_body)
        # condition fails and there's an else-body
        elif (len(statement)==3):
            else_body = statement[2]
            self.run_statement(else_body)

    #TODO: Implement while statement.
    def __execute_while_statement(self, statement):             # [while, [[condition], [body]]]
        itp = Interpreter()
        condition_result = evaluate_expression(statement[0])
        
        # condition is not a boolean
        if(condition_result != itp.TRUE_DEF and condition_result != itp.FALSE_DEF):
            itp = Interpreter()
            itp.error(1, "Condition of the if statement must evaluate to a boolean type.")

        
test = Interpreter()
test.run(file_contents)
