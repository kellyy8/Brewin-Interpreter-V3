from intbase import InterpreterBase, ErrorType
from bparser import BParser

# TODO: Check which functions to change to private member functions later. Currently implementing some as public methods.

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

class ClassDefinition:
    def __init__(self, name, definition, interpreter):
        # store each class's name (help with type checking later?) & their methods (list) and fields (list)
        self.class_name = name
        self.my_methods = {}
        self.my_fields = {}
        self.itp = interpreter

        for item in definition:
            if item[0] == self.itp.FIELD_DEF:                           #{'field': ['field_name', 'init_value']}
                if(item[1] in self.my_fields):
                    self.itp.error(ErrorType.NAME_ERROR, "Fields cannot share the same name.")
                self.my_fields[item[1]] = item[2]
            elif item[0] == self.itp.METHOD_DEF:                        #{'method': ['method_name', ['params'], ['top-level statement']]}
                if(item[1] in self.my_methods):
                    self.itp.error(ErrorType.NAME_ERROR, "Methods cannot share the same name.")
                self.my_methods[item[1]] = item[2:]

    # use definition of a class to create & return an instance of object
    # TODO: Consider instantiating a Variable and Value object when creating an instance to implement PBV.
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
    # store all variables (accounts for shadowing...)
    def __init__(self, method_def, object):
        self.visible_variables = object.my_fields
        self.method_def = method_def

    def __add_variables(self, name, val):
        self.visible_variables[name] = val

class ObjectDefinition:
    def __init__(self, interpreter):
        self.my_methods = {}                                   #{'method_name' : ['params'], ['top-level statement']}
        self.my_fields = {}                                    #{'field_name' : 'init_value' (can hold curr value later too)}
        self.itp = interpreter

    # map 'method' to its 'definition'
    # TODO: Do I need a deep copy of method def? So it doesn't affect the parameters for other objects with same method? TEST
    def add_method(self, method_name, method_def):
        self.my_methods[method_name] = method_def
    
    # map 'field' to its 'initial value'
    # TODO: Do I need a deep copy of field names? So it doesn't affect the fields for other objects with same field names? TEST
    def add_field(self, name, init_val):
        self.my_fields[name] = init_val

    # JUST FOR MAIN() IN MAIN CLASS.
    def call_main_method(self, method_name):
        method_def = self.__find_method(method_name)
        top_level_statement = self.get_top_level_statement(method_def)
        result = self.__run_statement(top_level_statement)
        return result[0]                                                    # Do I ever do anything with this result?

    # Find method's definition by method name.
    def __find_method(self, method_name):                                  # returns: [['params'], ['top-level statement']]
        return self.my_methods.get(method_name)
    
    # Get top_level statement (single statement or 'begin' with substatements).
    def get_top_level_statement(self, method_def):
        return method_def[1]
    
    # runs/interprets the passed-in statement until completion and gets the result, if any
    def __run_statement(self, statement, in_scope_vars=None):
        # in_scope_vars = self.my_fields by default --> arg passed in if there are params in addition to fields that are visible
        if(in_scope_vars is None):
            in_scope_vars = self.my_fields
        
        # ('return value', termination indicator) ('return value' extracted in 'call expressions')
        result = ('', False)
        if statement[0] == self.itp.PRINT_DEF:
            self.__execute_print_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.INPUT_INT_DEF:
            self.__execute_input_int_statement(statement[1], in_scope_vars)
        elif statement[0] == self.itp.INPUT_STRING_DEF:
            self.__execute_input_str_statement(statement[1], in_scope_vars)
        elif statement[0] == self.itp.IF_DEF:
            result = self.__execute_if_statement(statement[1:], in_scope_vars)        
        elif statement[0] == self.itp.WHILE_DEF:
            result = self.__execute_while_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.RETURN_DEF:
            # HANDLE TERMINATION
            if(len(statement)==2):
                result = self.__execute_return_statement(statement[1], in_scope_vars)
            else:
                result = ('', True)
        elif statement[0] == self.itp.BEGIN_DEF:
            result = self.__execute_all_sub_statements_of_begin_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.SET_DEF:
            self.__execute_set_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.CALL_DEF:
            result = self.__execute_call_statement(statement[1:], in_scope_vars)

        return result
    
    def __get_const_or_var_val(self, expr, in_scope_vars):
        # if expression is a string, bool, null, or neg/pos int constant:
        if(expr[0]=='"' or expr==self.itp.TRUE_DEF or expr==self.itp.FALSE_DEF or expr==self.itp.NULL_DEF or expr=='-' or expr.isnumeric()):
            return expr
        # else: expression is a variable ==> retrieve and return its value IFF variable exists
        else:
            val = in_scope_vars.get(expr)
            if(val is None):
                self.itp.error(ErrorType.NAME_ERROR, f"No variable with the name '{expr}'.")
            else:
                return val
            
    # Variables can hold constants and object references. 
    def __convert_operands_from_parsed_form(self, op):
        if (type(op) == ObjectDefinition):
            return op
        elif op[0] == '"':
            return op[1:-1]
        elif op == self.itp.TRUE_DEF:
            return True
        elif op == self.itp.FALSE_DEF:
            return False
        elif op == self.itp.NULL_DEF:
            return None
        else:
            return int(op)

    # TODO: Test if this works with everything that uses expressions/this function.
    def __evaluate_expression(self, expression, in_scope_vars):    #return int/string ('""')/bool constants as strings, or an object reference
        # expr examples = ['true'] ['num'] ['>', 'n', '0'], ['*', 'n', 'result'], ['call', 'me', 'factorial', 'num']

        # expression is a constant or variable
        if(type(expression)!=list):
            return self.__get_const_or_var_val(expression, in_scope_vars)
        
        # TODO: Test if expression is returned, and if its format is in parsed format. Return value must be in ''.
        # expression is function 'call' statement (funcs can return nothing or what eval_expr can return)
        if(expression[0]==self.itp.CALL_DEF):
            returned_val = self.__execute_call_statement(expression[1:], in_scope_vars)
            return returned_val[0]
        
        # expression is 'new' object instantiation
        if(expression[0]==self.itp.NEW_DEF):                         # [new, class_name]
            class_def = self.itp.__find_class_definition__(expression[1])
            if(class_def is None):
                self.itp.error(ErrorType.TYPE_ERROR, f"No class with the name: '{expression[1]}'.")         #page 23 of spec
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

                # set up operand for nested expressions: returned value of function, variable, or constant
                if type(op)==list:
                    op = self.__evaluate_expression(op, in_scope_vars)
                else:
                    op = self.__get_const_or_var_val(op, in_scope_vars)

                if op!=self.itp.TRUE_DEF and op!=self.itp.FALSE_DEF:
                    self.itp.error(ErrorType.TYPE_ERROR, "Unary operations only works with boolean operands.")
                elif op==self.itp.TRUE_DEF:
                    stack.append(self.itp.FALSE_DEF)
                else:
                    stack.append(self.itp.TRUE_DEF)
            # perform operation
            elif expr in all_ops:
                op1 = stack.pop()
                op2 = stack.pop()

                # set up operand for nested expressions: returned value of function, variable, or constant
                if type(op1)==list:
                    op1 = self.__evaluate_expression(op1, in_scope_vars)
                else:
                    op1 = self.__get_const_or_var_val(op1, in_scope_vars)

                if type(op2)==list:
                    op2 = self.__evaluate_expression(op2, in_scope_vars)
                else:
                    op2 = self.__get_const_or_var_val(op2, in_scope_vars)

                # Convert op1 and op2 into int, string, or bool constants, null, or object reference.
                op1 = self.__convert_operands_from_parsed_form(op1)
                op2 = self.__convert_operands_from_parsed_form(op2)

                # TODO: Do more test cases for incompatibilities.
                # check for type compatibility & operand compatibility
                if expr=='+' and not(type(op1)==int and type(op2)== int) and not(type(op1)==str and type(op2)==str):
                    self.itp.error(ErrorType.TYPE_ERROR, "'+' only works with integers and strings.")
                elif expr in math_ops and (type(op1) != int or type(op2) != int):
                    self.itp.error(ErrorType.TYPE_ERROR, "Math operations only compatible with integers.")
                elif expr in compare_ops:
                    if (expr in only_bool_compare_ops):
                        if not (type(op1)==bool and type(op2)==bool):
                            self.itp.error(ErrorType.TYPE_ERROR, "Logical AND and OR operations only compatible with booleans.")
                    elif (expr in only_int_and_str_compare_ops):
                        if not(type(op1)==int and type(op2)==int) and not(type(op1)==str and type(op2)==str):
                            self.itp.error(ErrorType.TYPE_ERROR, "Operands must both be integers or strings.")
                    else:
                        # TODO: Do more test cases for this.
                        # Return error if operands do not match, and neither operands are 'null'.
                        if(type(op1)!=type(op2)):
                            if(op1 is not None and op2 is not None):
                                self.itp.error(ErrorType.TYPE_ERROR, "Operands must match for '==' or '!='. Null vs object reference are the only exceptions.")

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
                    if(result): result = self.itp.TRUE_DEF
                    else: result = self.itp.FALSE_DEF

                stack.append(result)

            # store operand into stack
            else:
                stack.append(expr)
            
        return stack.pop()

    def __execute_print_statement(self, statement, in_scope_vars):    # prints: consts, vars, expr; no object refs nor null
        output = ""
        for arg in statement:
            # expressions evaluating to str, int, bool values wrapped in ''
            result = self.__evaluate_expression(arg, in_scope_vars)
            if(len(result)>0 and result[0]=='"'):
                result = result[1:-1]
            output += result
        self.itp.output(output)
    
    #ASSUMING inputi/s gets the right reference variables.
    def __execute_input_int_statement(self, statement, in_scope_vars):
        var = statement
        val = self.itp.get_input()
        in_scope_vars[var] = val

    def __execute_input_str_statement(self, statement, in_scope_vars):
        var = statement
        val = '"' + self.itp.get_input() + '"'
        in_scope_vars[var] = val

    def __execute_if_statement(self, statement, in_scope_vars):            # [if, [[condition], [if-body], [else-body]]]
        condition_result = self.__evaluate_expression(statement[0], in_scope_vars)
        if_body = statement[1]
        returned_val = ('', False)

        # condition is not a boolean
        if(condition_result != self.itp.TRUE_DEF and condition_result != self.itp.FALSE_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        # condition passes
        elif(condition_result == self.itp.TRUE_DEF):
            # HANDLE TERMINATION
            if(if_body[0]==self.itp.RETURN_DEF):
                return self.__run_statement(if_body[0:len(if_body[0])], in_scope_vars)
            if(returned_val[1]==False):
                return self.__run_statement(if_body, in_scope_vars)
        # condition fails and there's an else-body
        elif (len(statement)==3):
            else_body = statement[2]
            # HANDLE TERMINATION
            if(else_body[0]==self.itp.RETURN_DEF):
                return self.__run_statement(else_body[0:len(else_body[0])], in_scope_vars)
            if(returned_val[1]==False):
                return self.__run_statement(else_body, in_scope_vars)
            return self.__run_statement(else_body, in_scope_vars)

    def __execute_while_statement(self, statement, in_scope_vars):             # [while, [condition], [body]]
        condition_result = self.__evaluate_expression(statement[0], in_scope_vars)
        returned_val = ('', False)
        # condition is not a boolean
        if(condition_result != self.itp.TRUE_DEF and condition_result != self.itp.FALSE_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        else:
            while(condition_result == self.itp.TRUE_DEF and returned_val[1]==False):
                # HANDLE TERMINATION
                if(statement[1][0]==self.itp.RETURN_DEF):
                    return self.__run_statement(statement[1][0:len(statement[1])], in_scope_vars)
                # Inner statements could return (?, True) --> terminates while loop
                returned_val = self.__run_statement(statement[1], in_scope_vars)
                condition_result = self.__evaluate_expression(statement[0], in_scope_vars)

                # another check --> since we run and use the condition again
                if(condition_result != self.itp.TRUE_DEF and condition_result != self.itp.FALSE_DEF):
                    self.itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        return returned_val

    def __execute_return_statement(self, statement, in_scope_vars):            # [return] or [return, [expression]]
        # HANDLE TERMINATION
        return (self.__evaluate_expression(statement, in_scope_vars), True)

    def __execute_all_sub_statements_of_begin_statement(self, statement, in_scope_vars):
        returned_val = ('', False)
        for substatement in statement:
            # HANDLE TERMINATION
            if(substatement[0]==self.itp.RETURN_DEF):
                return self.__run_statement(substatement[0:len(substatement[0])], in_scope_vars)  # sets returned_val[1] to True
            # block remaining statements; returned_val does not update (holds onto true return val)
            # outer 'begin' statements will terminate after inner statements terminated
            if(returned_val[1]==False):
                returned_val = self.__run_statement(substatement, in_scope_vars)
        return returned_val
        
    def __execute_set_statement(self, statement, in_scope_vars):               # [set, var_name, new_value]
        var_name = statement[0]
        new_val = statement[1]

        # ASSUMING in_scope_vars contains the right object references
        if var_name in in_scope_vars:
            new_val = self.__evaluate_expression(new_val, in_scope_vars)  # eval_expr() handles everything set receives as new_val arg
            in_scope_vars[var_name] = new_val
        else:
            self.itp.error(ErrorType.NAME_ERROR, f"No variable with the name '{var_name}'.")
            
    # TODO: Ensure pass by value effect for object's fields & nested function call's parameters.
    def __execute_call_statement(self, statement, parent_scope_vars):         # ['call', 'target_object', 'method_name', arg1, arg2, ..., argN]
        target_object_name = statement[0]
        method_name = statement[1]

        # At least 1 argument passed in.
        if(len(statement) > 2):
            arguments = statement[2:]
        # No arguments passed in.
        else:
            arguments = []

        # 'target_object_name' is either 'me' or a member variable that holds an object reference.
        # Use 'self' to find method or retrieve 'object reference' get its method's definition.
        if(target_object_name == self.itp.ME_DEF):
            method_def = self.__find_method(method_name)
        else:
            # retrieve value from variable
            target_object = self.__evaluate_expression(target_object_name, self.my_fields)
            # check if value is an object reference
            if(type(target_object) != ObjectDefinition):
                self.itp.error(ErrorType.FAULT_ERROR, "Target object must be an object reference.")
            # use object reference
            method_def = target_object.__find_method(method_name)

        # Check if method is undefined.
        if(method_def is None):
            self.itp.error(ErrorType.NAME_ERROR, f"Cannot find method with the name '{method_name}'.")

        # Check if number of arguments matches number of parameters.
        parameters = method_def[0]
        if(len(parameters) != len(arguments)):
            self.itp.error(ErrorType.TYPE_ERROR, f"You passed in {len(arguments)} argument(s) for {len(parameters)} parameter(s).")

        # TODO: Check pass by value effect.
        
        # method_obj = MethodDefinition(method_def)
        # for name, val in target_object.my_fields.items():
        #     method_obj.__add_variables(name, val)
        # for i in range(len(parameters)): #accounts for shadowing
        #     method_obj.__add_variables([parameters[i]], arguments[i])

        # i think the way i am doing this will create new object references (allowing for pass by value)
        # actually idk cus doesn't it return the constant and values directly back to me (same id's)

        # Arguments can be constants, variables, or expressions. Process them with parent's scope before creating new lexical environment.
        eval_args = []
        for arg in arguments:
            eval_args.append(self.__evaluate_expression(arg, parent_scope_vars))

        # TODO: Consider creating Variable and Value object pairs as well to implement PBV for parameters.
        # (concerning race condition, even tho parameters are always reinitialized, if there's multithreading, parameters used for each method call should still be independent.)
        # TODO: Check later that I am creating a brand new dictionary for each method call.

        # Map parameters to arguments; add them to dictionary of visible variables (in-scope) for method call (make lex enviro)
        # Fields are always in-scope, unless shadowed.
        if(target_object_name == self.itp.ME_DEF):
            visible_vars = self.my_fields
        else:
            visible_vars = target_object.my_fields

        # Initialize and add parameters to in-scope variables. Accounts for parameters shadowing fields. 
        # I think the parameter names are shared across all objects of same class,
        # but this key is creating a new pool of visible variables for each method call, so PBV should still hold. 
        for i in range(len(parameters)):
            visible_vars[parameters[i]] = eval_args[i]

        # TODO: HOW DO I KNOW THAT THIS 'RUN' WORKS WITH THE arguments/assigned parameters?
        top_level_statement = self.get_top_level_statement(method_def)
        
        # HANDLE TERMINATION
        if(top_level_statement[0]==self.itp.RETURN_DEF):
            return self.__run_statement(top_level_statement[0:len(top_level_statement[0])], visible_vars)
        return self.__run_statement(top_level_statement, visible_vars)


# filename = "/Users/kellyyu/Downloads/23SP/CS131/P1/spring-23-autograder/brew.txt"
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
