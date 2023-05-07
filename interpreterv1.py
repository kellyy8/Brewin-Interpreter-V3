from intbase import InterpreterBase, ErrorType
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

# test_statement = ['if', ['==', '0', ['%', '4', '2']], ['print', '"x is even"'], ['print', '"x is odd"']]

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase’s constructor
        self.classes = {}

    # map classes to their definitions
    def __track_all_classes__(self, parsed_program):
        for class_def in parsed_program:
            if class_def[1] in self.classes:
                super().error(ErrorType.TYPE_ERROR, "Duplicate classes not allowed.")
            self.classes[class_def[1]] = class_def[2:]                                      # {'class_name' : ['class_def']}

    # returns a list containing a particular class's definition
    # TODO: Return something else if class_name is not a key (class does not exist)
    def __find_class_definition__(self, class_name):
        return self.classes.get(class_name)                                                 # returns: ['class_def']
    
    def run(self, program):
        # parse the program into a more easily processed form
        result, parsed_program = BParser.parse(program)
        if result == False:
            return super().error(ErrorType.SYNTAX_ERROR, "Failed to parse file.")            #TODO: Check if this is the right ERROR_TYPE.
        else:
            print(parsed_program)
            print("-------------------------------------------------------------------------------------------------------------")
            self.__track_all_classes__(parsed_program)
            class_def = self.__find_class_definition__("main")

            # create a "main" class --> create object of type "main" --> call object's "main" method
            main_class = ClassDefinition("main", class_def, self)
            main_obj = main_class.instantiate_object()
            main_obj.call_method("main")
            # main_obj.run_statement(test_statement)

class ClassDefinition:
    # constructor for a ClassDefinition
    def __init__(self, name, definition, interpreter):
        # store each class's name (help with type checking later?) & their methods (list) and fields (list)
        self.class_name = name
        self.my_methods = {}
        self.my_fields = {}
        self.itp = interpreter

        for item in definition:
            if item[0] == 'field':                           #{'field': ['field_name', 'init_value']}
                if(item[1] in self.my_fields):
                    self.itp.error(ErrorType.NAME_ERROR, "Fields cannot share the same name.")
                self.my_fields[item[1]] = item[2]
            elif item[0] == 'method':                        #{'method': ['method_name', ['params'], ['top-level statement']]}
                if(item[1] in self.my_methods):
                    self.itp.error(ErrorType.NAME_ERROR, "Methods cannot share the same name.")
                self.my_methods[item[1]] = item[2:]

    # use definition of a class to create & return an instance of object
    def instantiate_object(self): 
        obj = ObjectDefinition(self.itp)
        for name, definition in self.my_methods.items():
            obj.add_method(name, definition)
        for name, init_val in self.my_fields.items():
            obj.add_field(name, init_val)
        return obj     

class ValueDefinition:
    def __init__(self, val):
        self.value = val

class VariableDefinition:
    # store 'value' objects
    def __init__(self, var):
        self.variable = var

class MethodDefinition:
    # store all variables (account for shadowing), 
    def __init__(self, method_def):
        self.visible_variables = {}
        self.method_def = method_def

    def __add_variables(self, name, val):
        self.visible_variables[name] = val

class ObjectDefinition:
    def __init__(self, interpreter):
        self.my_methods = {}                                   #{'method_name' : ['params'], ['top-level statement']}
        self.my_fields = {}                                    #{'field_name' : 'init_value' (can hold curr value later too)}
        # self.terminate_function = False
        self.itp = interpreter

    # map 'method' to its 'definition'
    # TODO: Do I need a deep copy of method def? So it doesn't affect the parameters for other objects with same method? TEST
    def add_method(self, method_name, method_def):
        self.my_methods[method_name] = method_def
    
    # map 'field' to its 'initial value'
    # TODO: Do I need a deep copy of field names? So it doesn't affect the fields for other objects with same field names? TEST
    def add_field(self, name, init_val):
        self.my_fields[name] = init_val

# IMPLEMENTed
    # Interpret the specified method using the provided parameters    
    # TODO: Where do I ask users for parameters? (i think this is just for main function)
    def call_method(self, method_name):
        """ √ method = self.__find_method(method_name)
            √ statement = method.get_top_level_statement()
             result = self.__run_statement(statement)
            √ return result """
        method_def = self.__find_method(method_name)
        top_level_statement = self.get_top_level_statement(method_def)
        result = self.run_statement(top_level_statement)                        #TODO: Privatize run_statement function.
        return result

    # find method's definition by method name
    def __find_method(self, method_name):                                  # returns: [['params'], ['top-level statement']]
        return self.my_methods.get(method_name)
    
    # get top level statement (single line or 'begin' with sublines)
    def get_top_level_statement(self, method_def):
        return method_def[1]
    
#   IMPLEMENTed

    # runs/interprets the passed-in statement until completion and gets the result, if any
    # TODO: Change all to private member functions later. Currently implementing some as public methods.
    def run_statement(self, statement):
        # if(self.terminate_function):
        #     return
        
        itp = Interpreter()
        if statement[0] == itp.PRINT_DEF:
            self.__execute_print_statement(statement[1:])
        # elif is_an_input_statement(statement):
        #     result = self.__execute_input_statement(statement)
        elif statement[0] == itp.IF_DEF:
            self.__execute_if_statement(statement[1:])        
        elif statement[0] == itp.WHILE_DEF:
            self.__execute_while_statement(statement[1:])
        elif statement[0] == itp.RETURN_DEF:
            #TODO: Must terminate function after this block.
            # self.terminate_function = True
            if(len(statement)==2):
                return self.__execute_return_statement(statement[1])
        elif statement[0] == itp.BEGIN_DEF:
            self.__execute_all_sub_statements_of_begin_statement(statement[1:])
        elif statement[0] == itp.SET_DEF:
            self.__execute_set_statement(statement[1:])
        elif statement[0] == itp.CALL_DEF:
            self.__execute_call_statement(statement[1:])
    
    def evaluate_expression(self, expression):    #return int/string ('""')/bool constants as strings, or an object reference
        # expr examples = ['true'] ['num'] ['>', 'n', '0'], ['*', 'n', 'result'], ['call', 'me', 'factorial', 'num']
        itp = Interpreter()

        if(type(expression)!=list):
            # TODO: if expression is a variable ==> retrieve and return its value
            # else expression is a constant (int, string '""', true/false, null) ==> return expression
            return expression
        
        # TODO: Test if expression is returned, and if its format is in parsed format. Return value must be in ''.
        # expression is function 'call' statement (funcs can return nothing or what eval_expr can return)
        if(expression[0]==itp.CALL_DEF):
            return self.__execute_call_statement(expression[1:])
        
        # TODO: Test with set statement.
        # expression is 'new' object instantiation
        if(expression[0]==itp.NEW_DEF):                         # [new, class_name]
            class_def = self.itp.__find_class_definition__(expression[1])
            if(class_def == None):
                self.itp.error(ErrorType.TYPE_ERROR, f"No class with the name: '{expression[1]}'.")
            class_obj = ClassDefinition(expression[1], class_def, self.itp)
            instance = class_obj.instantiate_object()
            return instance

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
            # 'expression' operand
            if type(expr)==list:
                stack.append(expr)
            # 'unary NOT' operand
            elif expr == '!':
                op = stack.pop()
                if op!=itp.TRUE_DEF and op!=itp.FALSE_DEF:
                    itp.error(ErrorType.TYPE_ERROR, "Unary operations only works with boolean operands.")
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
                    op1 = self.evaluate_expression(op1)
                # TODO: Get value from existing variables (parameters or fields).
                # otherwise, op1 is a constant

                if type(op2)==list:
                    op2 = self.evaluate_expression(op2)
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
                    itp.error(ErrorType.TYPE_ERROR, "'+' only works with integers and strings.")
                elif expr in math_ops and (type(op1) != int or type(op2) != int):
                    itp.error(ErrorType.TYPE_ERROR, "Math operations only compatible with integers.")
                elif expr in compare_ops:
                    if (expr in only_bool_compare_ops):
                        if not (type(op1)==bool and type(op2)==bool):
                            itp.error(ErrorType.TYPE_ERROR, "Logical AND and OR operations only compatible with booleans.")
                    elif (expr in only_int_and_str_compare_ops):
                        if not(type(op1)==int and type(op2)==int) and not(type(op1)==str and type(op2)==str):
                            itp.error(ErrorType.TYPE_ERROR, "Operands must both be integers or strings.")
                    else:
                        if op1!=None and op2!=None and not(type(op1)==int and type(op2)==int) and not(type(op1)==str and type(op2)==str) and not(type(op1)==bool and type(op2)==bool):
                            itp.error(ErrorType.TYPE_ERROR, "Operands must match for '==' or '!='.")

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

    def __execute_print_statement(self, statement):     #not printing object refs or null
        output = ""
        for arg in statement:
            # expressions evaluating to str, int, bool values wrapped in ''
            if type(arg)==list:
                result = self.evaluate_expression(arg)
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
        
        self.itp.output(output)
    
    def __execute_if_statement(self, statement):            # [if, [[condition], [if-body], [else-body]]]
        itp = Interpreter()
        condition_result = self.evaluate_expression(statement[0])
        if_body = statement[1]

        # condition is not a boolean
        if(condition_result != itp.TRUE_DEF and condition_result != itp.FALSE_DEF):
            itp = Interpreter()
            itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        # condition passes
        elif(condition_result == itp.TRUE_DEF):
            self.run_statement(if_body)
        # condition fails and there's an else-body
        elif (len(statement)==3):
            else_body = statement[2]
            self.run_statement(else_body)

    # TODO: Test this when set command works.
    def __execute_while_statement(self, statement):             # [while, [condition], [body]]
        itp = Interpreter()
        condition_result = self.evaluate_expression(statement[0])
        
        # condition is not a boolean
        if(condition_result != itp.TRUE_DEF and condition_result != itp.FALSE_DEF):
            itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        elif(condition_result == itp.TRUE_DEF):
            self.run_statement(statement[1])

    # TODO: Test this when I get expression to work with function calls.
    def __execute_return_statement(self, statement):            # [return] or [return, [expression]]
        return self.evaluate_expression(statement)

    def __execute_all_sub_statements_of_begin_statement(self, statement):
        for substatement in statement:
            self.run_statement(substatement)
        
    # TODO: Test if all valid values are evaluated right, and if only 1 variable is updated each time.
    def __execute_set_statement(self, statement):               # [set, var_name, new_value]
        var_name = statement[0]
        new_val = statement[1]
        # search for parameter/field with var_name
        # if variable not found, return NAME_ERROR
        # else evaluate and update value   <---------- function handles constants, vars, and expr
        new_val = self.evaluate_expression(new_val)

    # TODO: Fix so it can work with fields and parameter values.
    def __execute_call_statement(self, statement):         # ['call', 'target_object', 'method_name', param1, param2, ..., paramn]
        itp = Interpreter()
        target_object = statement[0]
        method_name = statement[1]
        arguments = statement[2:]

        # Use 'self' to find method or 'object reference' to get method's definition.
        if(target_object == 'null'):                 #TODO: Check if == 'null' or == None; prolly null cus we get obj ref from eval expressions only..right?
            itp.error(ErrorType.FAULT_ERROR, "Target object cannot be null. Must be object reference or 'me'.")
        elif(target_object == 'me'):
            method_def = self.__find_method(method_name)
        #TODO: Get the object reference based on passed in name.
        else:
            method_def = target_object.__find_method(method_name)

        # Check if method is undefined.
        if(method_def==None):
            itp.error(ErrorType.NAME_ERROR, f"Cannot find method with the name '{method_name}'.")

        # Check if number of arguments matches number of parameters.
        parameters = method_def[0]
        if(len(parameters) != len(arguments)):
            itp.error(ErrorType.TYPE_ERROR, f"You passed in {len(arguments)} argument(s) for {len(parameters)} parameter(s).")
        # Initialize all parameters.
        # TODO: Check pass by value effect.
        
        # method_obj = MethodDefinition(method_def)
        # for name, val in target_object.my_fields.items():
        #     method_obj.__add_variables(name, val)
        # for i in range(len(parameters)): #accounts for shadowing
        #     method_obj.__add_variables([parameters[i]], arguments[i])
        
        else:
            # map parameters to arguments (their values)
            param_to_val = {}
            for i in range(len(parameters)):
                param_to_val[parameters[i]] = arguments[i]

        # # TODO: HOW DO I KNOW THAT THIS 'RUN' WORKS WITH THE arguments/assigned parameters? it's not lol
        top_level_statement = self.get_top_level_statement(method_def)
        return self.run_statement(top_level_statement) #only statement that returns from run_statement? to return expression or nothing


test = Interpreter()
test.run(file_contents)
