from intbase import InterpreterBase, ErrorType
from ValueDefinitionv2 import ValueDefinition
from VariableDefinitionv2 import VariableDefinition

# parser:
# [ 'field', 'type_name', 'field_name', 'init_value']
# [ 'method', 'return_type', 'name', [[type1, param1], [type2, param2], ..], ['top-level statement'] ]

# When assigning a value to a variable (field init, param init, reassignment), define a value_def object for the value.
def create_value_object(val):
    # values can be primitives (int, string, bool), object references (class/subclass), or null
    if (type(val) == ObjectDefinition):
        return ValueDefinition(InterpreterBase.CLASS_DEF, val, val.get_object_type())
    elif val == InterpreterBase.NULL_DEF:
        return ValueDefinition(InterpreterBase.CLASS_DEF, val)
    elif val[0] == '"':
        return ValueDefinition(InterpreterBase.STRING_DEF, val)
    elif val == InterpreterBase.TRUE_DEF or val == InterpreterBase.FALSE_DEF:
        return ValueDefinition(InterpreterBase.BOOL_DEF, val)
    else:
        return ValueDefinition(InterpreterBase.INT_DEF, val)

def create_var_object(var_type, var_name):
    # variable holds primitives (int, string, bool)
    if(var_type == InterpreterBase.INT_DEF or var_type == InterpreterBase.STRING_DEF or var_type == InterpreterBase.BOOL_DEF):
        return VariableDefinition(var_type, var_name)
    # variable holds object references (store class name)
    else:
        return VariableDefinition(InterpreterBase.CLASS_DEF, var_name, var_type)
    
class ObjectDefinition:
    def __init__(self, interpreter, class_name, class_def):
        self.class_name = class_name
        self.my_methods = {}                                   #{ 'method_name' : 'return_type', [[type1, param1], [type2, param2], ..], ['top-level statement'] }
        self.my_fields = {}                                    #{ 'field_name' : (var_def object, value_def object) }
        self.itp = interpreter

        # populate object definition with class definition
        for item in class_def:
            if item[0] == self.itp.FIELD_DEF:
                type_name = item[1]
                field_name = item[2]
                init_val = item[3]

                if(field_name in self.my_fields):
                    self.itp.error(ErrorType.NAME_ERROR, "Fields cannot share the same name.")
                # map field name to a value with type tag
                else:
                    # TYPE CHECKING FIELD INITIALIZATION:
                    field_var = create_var_object(type_name, field_name)
                    init_val = create_value_object(init_val)

                    field_var_type = field_var.get_type()                       # do this because it's gonna be diff from type_name if field holds object references
                    init_val_type = init_val.get_type()
                    #TODO: This does not account for polymorphism yet. Not yet comparing class names if type == CLASS_DEF
                    # Types (int, string, bool, class) should match.
                    if(init_val_type != field_var_type):
                        self.itp.error(ErrorType.TYPE_ERROR, f"Field of type '{field_var_type}' cannot be initialized with a value of type '{init_val_type}'.")
                    # Otherwise, value is primitive or null. Null can be assigned to any variables holding any type of object reference.
                    # For fields, values are not object references. They are either constants or null.
                    else:
                        self.my_fields[field_name] = (field_var, init_val)
            
            elif item[0] == self.itp.METHOD_DEF:
                method_name = item[2]
                if(method_name in self.my_methods):
                    self.itp.error(ErrorType.NAME_ERROR, "Methods cannot share the same name.")
                # map method name to its whole definition (return, params, statements)
                else:
                    # TODO: Update to BREWIN++ version later.
                    self.my_methods[method_name] = [item[1]] + item[3:]   # BREWIN++ version
                    # self.my_methods[method_name] = item[3:]                 # BREWIN version

        # print("MY FIELDS:")
        # for k, v in self.my_fields.items():
        #     print(k, ":", v[0].get_type(), v[0].get_name(), "= ", v[1].get_type(), v[1].get_value())
        # print("MY METHODS:")
        # for k, v in self.my_methods.items():
        #     print(k, ":", v)

    def get_object_type(self):
        return self.class_name

    # JUST FOR MAIN() IN MAIN CLASS.
    def call_main_method(self, method_name):
        method_def = self.__find_method(method_name)

        # TODO: Check if this check is needed. I think so bc it's like calling any other method. Check if method exists or else name error. Matches barista right now.
        if method_def is None:
            self.itp.error(ErrorType.NAME_ERROR, "Cannot find method with the name 'main'.")

        top_level_statement = self.get_top_level_statement(method_def)
        result = self.__run_statement(top_level_statement)
        # MARK
        return result[0]                                                    # Do I ever do anything with this result?

    # Find method's definition by method name.
    def __find_method(self, method_name):                                  # returns: ['return_type', [[type1, param1], [type2, param2], ..], ['top-level statement']]
        return self.my_methods.get(method_name)
    
    # Get top_level statement (single statement or 'begin' with substatements).
    def get_top_level_statement(self, method_def):
        return method_def[2]                                                # method_def = ['return_type', [[params]], [top level statement]]

    # runs/interprets the passed-in statement until completion and gets the result, if any
    def __run_statement(self, statement, in_scope_vars=None):
        # in_scope_vars = [self.my_fields] by default --> arg passed in if there are params in addition to fields that are visible
        # MARK
        if(in_scope_vars is None):
            in_scope_vars = [self.my_fields]
        
        # ('return value', termination indicator) ('return value' extracted in 'call expressions')
        # MARK - RETURNED_VAL
        returned_val = (None, False)
        if statement[0] == self.itp.PRINT_DEF:
            self.__execute_print_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.INPUT_INT_DEF:
            self.__execute_input_int_statement(statement[1], in_scope_vars)
        elif statement[0] == self.itp.INPUT_STRING_DEF:
            self.__execute_input_str_statement(statement[1], in_scope_vars)
        elif statement[0] == self.itp.IF_DEF:
            returned_val = self.__execute_if_statement(statement[1:], in_scope_vars)        
        elif statement[0] == self.itp.WHILE_DEF:
            returned_val = self.__execute_while_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.RETURN_DEF:
            # HANDLE TERMINATION
            if(len(statement)==2):
                returned_val = self.__execute_return_statement(statement[1], in_scope_vars)
            else:
                returned_val = (None, True)
        elif statement[0] == self.itp.BEGIN_DEF:
            returned_val = self.__execute_all_sub_statements_of_begin_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.SET_DEF:
            self.__execute_set_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.CALL_DEF:
            returned_val = self.__execute_call_statement(statement[1:], in_scope_vars)

        # LOCAL VARIABLES -- LET STATEMENT
        # TODO: Check if it should return a value.
        elif statement[0] == self.itp.LET_DEF:
            returned_val = self.__execute_let_statement(statement[1:], in_scope_vars)

        return returned_val
    
    def __get_const_or_var_val(self, expr, in_scope_vars):
        # MARK -- DEPENDS ON HOW EXPR IS PASSED IN OMG
        # if expression is a string, bool, null, or neg/pos int constant:
        if(expr[0]=='"' or expr==self.itp.TRUE_DEF or expr==self.itp.FALSE_DEF or expr==self.itp.NULL_DEF or expr[0]=='-' or expr.isnumeric()):
            return expr
        # else: expression is a variable ==> retrieve and return its value IFF variable exists
        else:
            # LIFO; search from most recently added dictionary
            for i in range(len(in_scope_vars)-1, -1, -1):
                scope_dict = in_scope_vars[i]
                var = scope_dict.get(expr)
                if(var is not None):
                    # extract the value from value_def object & return it; ends loop and function (no error)
                    value_obj = var[1]
                    # print("value:", value_obj.get_value())
                    return value_obj.get_value()
            
            # this line only runs if we searched through each scope dictionary and did not find variable with such name
            self.itp.error(ErrorType.NAME_ERROR, f"No variable with the name '{expr}'.")
            
    # Variables can hold constants and object references. 
    def __convert_operands_from_parsed_form(self, op):
        # MARK -- DEPENDS ON HOW OP IS PASSED IN.
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

    # MARK
    def __evaluate_expression(self, expression, in_scope_vars):    #return int/string ('""')/bool constants as strings, or an object reference
        # expr examples = ['true'] ['num'] ['>', 'n', '0'], ['*', 'n', 'result'], ['call', 'me', 'factorial', 'num']

        # expression is a constant or variable
        if(type(expression)!=list):
            return self.__get_const_or_var_val(expression, in_scope_vars)
        
        # expression is function 'call' statement (funcs can return nothing or what eval_expr can return)
        if(expression[0]==self.itp.CALL_DEF):
            returned_val = self.__execute_call_statement(expression[1:], in_scope_vars)
            return returned_val[0]
        
        # expression is 'new' object instantiation
        if(expression[0]==self.itp.NEW_DEF):                         # [new, class_name]
            class_def = self.itp.__find_class_definition__(expression[1])
            if(class_def is None):
                self.itp.error(ErrorType.TYPE_ERROR, f"No class with the name: '{expression[1]}'.")         #page 23 of spec
            
            instance = ObjectDefinition(self.itp, class_def)
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


                # TODO: Check what operands object references (classes/subclasses) are compatible with & handle polymorphism.
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
    # TODO: Store value_def objects rather than values into variables. (Do we have to check the variable's type matches int/str?) No..
    def __execute_input_int_statement(self, statement, in_scope_vars):
        var_name = statement
        new_val = self.itp.get_input()

        new_val = create_value_object(new_val)

        # ASSUMING that var_name is valid (there is a variable with that name for sure)
        # grab var_def object for type checking --> LIFO; search from most recently added dictionary
        which_dict = None
        for i in range(len(in_scope_vars)-1, -1, -1):
            scope_dict = in_scope_vars[i]
            var = scope_dict.get(var_name)          # var = (var_def object, val_def object)
            if(var is not None):
                # grab var_def object and break out of loop
                var = var[0]
                which_dict = i
        
        # TYPE CHECKING ASSIGNMENTS:
        if(var.get_type() != InterpreterBase.INT_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, f"Variable is of type '{var.get_type()}', not 'int'.")
        
        # TODO: Check: don't we assume that input is of correct type?
        elif(new_val.get_type() != InterpreterBase.INT_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, f"Variable expects 'int', but value is of type '{new_val.get_type()}'.")

        # update var_def object with val_def object
        in_scope_vars[which_dict][var_name] = (var, new_val)

    def __execute_input_str_statement(self, statement, in_scope_vars):
        var_name = statement
        new_val = '"' + self.itp.get_input() + '"'

        new_val = create_value_object(new_val)

        # ASSUMING that var_name is valid (there is a variable with that name for sure)
        # grab var_def object for type checking --> LIFO; search from most recently added dictionary
        which_dict = None
        for i in range(len(in_scope_vars)-1, -1, -1):
            scope_dict = in_scope_vars[i]
            var = scope_dict.get(var_name)          # var = (var_def object, val_def object)
            if(var is not None):
                # grab var_def object and break out of loop
                var = var[0]
                which_dict = i

        # TYPE CHECKING ASSIGNMENTS:
        if(var.get_type() != InterpreterBase.STRING_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, f"Variable is of type '{var.get_type()}', not 'string'.")
        
        # TODO: Check: don't we assume that input is of correct type?
        elif(new_val.get_type() != InterpreterBase.STRING_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, f"Variable expects 'string', but value is of type '{new_val.get_type()}'.")

        # update var_def object with val_def object
        in_scope_vars[which_dict][var_name] = (var, new_val)

    def __execute_if_statement(self, statement, in_scope_vars):            # [if, [[condition], [if-body], [else-body]]]
        condition_result = self.__evaluate_expression(statement[0], in_scope_vars)

        # condition is not a boolean
        if(condition_result != self.itp.TRUE_DEF and condition_result != self.itp.FALSE_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        # condition passes
        elif(condition_result == self.itp.TRUE_DEF):
            if_body = statement[1]
            # HANDLE TERMINATION
            if(if_body[0]==self.itp.RETURN_DEF):
                # runs return statement; returns (None or value, True)
                return self.__run_statement(if_body[0:len(if_body[0])], in_scope_vars)
            else:
                # propagates returned_val tuple up
                return self.__run_statement(if_body, in_scope_vars)
        # condition fails and there's an else-body
        elif (len(statement)==3):
            else_body = statement[2]
            # HANDLE TERMINATION
            if(else_body[0]==self.itp.RETURN_DEF):
                # runs return statement; returns (None or value, True)
                return self.__run_statement(else_body[0:len(else_body[0])], in_scope_vars)
            else:
                # propagates returned_val tuple up
                return self.__run_statement(else_body, in_scope_vars)
        # condition fails and there's NO else-body
        else:
            # return empty string (aka nothing); if no if/else body ran, no return statement would have ran & no value returned
            returned_val = (None, False)
            return returned_val

    def __execute_while_statement(self, statement, in_scope_vars):             # [while, [condition], [body]]
        condition_result = self.__evaluate_expression(statement[0], in_scope_vars)
        returned_val = (None, False)

        # condition is not a boolean
        if(condition_result != self.itp.TRUE_DEF and condition_result != self.itp.FALSE_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        else:
            while(condition_result == self.itp.TRUE_DEF and returned_val[1]==False):
                # HANDLE TERMINATION
                if(statement[1][0]==self.itp.RETURN_DEF):
                    # runs return statement; returns (None or value, True); terminates while loop
                    return self.__run_statement(statement[1][0:len(statement[1])], in_scope_vars)

                # propagates returned_val tuple up (after while loop is done)
                returned_val = self.__run_statement(statement[1], in_scope_vars)
                condition_result = self.__evaluate_expression(statement[0], in_scope_vars)

                # another check --> since we run and use the condition again
                if(condition_result != self.itp.TRUE_DEF and condition_result != self.itp.FALSE_DEF):
                    self.itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        
        # if while loop ran, propagates (possibly updated) returned_val tuple up
        # else, the while loop returns (None, False) for sure since no return statement ran
        return returned_val

    def __execute_return_statement(self, statement, in_scope_vars):            # [return] or [return, [expression]]
        # HANDLE TERMINATION
        return (self.__evaluate_expression(statement, in_scope_vars), True)

    def __execute_all_sub_statements_of_begin_statement(self, statement, in_scope_vars):
        # initially returned_val[1] == False since we just entered the begin statement (no return statement could have ran)
        returned_val = (None, False)

        for substatement in statement:
            # HANDLE TERMINATION
            if(substatement[0]==self.itp.RETURN_DEF):
                # runs return statement; returns (None or value, True)
                return self.__run_statement(substatement[0:len(substatement[0])], in_scope_vars)
            
            # addresses all cases where return statement is not the top-level statement (must be inside a begin statement)
                # if return statement is top-level statement, we have handled in if, while, begin, and call already
            # ^^ if such return statements ran, then the begin statement that contains the return statement must signal
            # any statements wrapping that begin statement to terminate as well (by not running any further statements in their scope)
            
            # outer statements will terminate after inner 'begin' statement terminated
            # returned_val[1] is set to True if inner statements ran a return statement
            if(returned_val[1]==False):
                returned_val = self.__run_statement(substatement, in_scope_vars)

            # no more statements should be ran since inner scope terminated 
            else:
                break

        # if a nested return statement ran, propagates returned_val tuple up
        # else, returns (None, False) for sure since no return statement ran
        return returned_val
        
    def __execute_set_statement(self, statement, in_scope_vars):               # [set, var_name, new_value]
        var_name = statement[0]
        new_val = statement[1]

        # LIFO; search from most recently added dictionary
        which_dict = None
        for i in range(len(in_scope_vars)-1, -1, -1):
            scope_dict = in_scope_vars[i]
            var = scope_dict.get(var_name)              # var = (var_def object, val_def object)
            
            # if variable exists:
            if (var is not None):
                which_dict = i
                # evaluate new value
                new_val = self.__evaluate_expression(new_val, in_scope_vars)  # eval_expr() handles everything set receives as new_val arg
                # create val_def object for new value
                new_val = create_value_object(new_val)
                new_val_type = new_val.get_type()

                # get variable's type (use var_def object)
                var_to_update = var[0]
                var_to_update_type = var_to_update.get_type()

                # TYPE CHECKING ASSIGNMENTS:
                # TODO: Need to handle polymorphism.
                if(new_val_type != var_to_update_type):
                    self.itp.error(ErrorType.TYPE_ERROR, f"Variable holds values of type '{var_to_update_type}', but value is of type '{new_val_type}'.")
                elif(new_val_type == InterpreterBase.CLASS_DEF and new_val != InterpreterBase.NULL_DEF):
                    print("CHECK FOR POLYMORPHISM HERE.")
                    # return
                # Otherwise, value is primitive or null. Null can be assigned to any variables holding any type of object reference.
                else:
                    # if it type checking passes, update the variable & return from function (don't run error statement)
                    in_scope_vars[which_dict][var_name] = (var_to_update, new_val)
                    print(var_to_update.get_type(), var_to_update.get_name(), "==>", new_val.get_type(), new_val.get_value())
                    return
    
        # this line only runs if the variable is not found (did not end & return from the loop early)
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

        # method_def == ['return_type', [[type1, param1], [type2, param2], ..], ['top-level statement']]

        # Check if number of arguments matches number of parameters.
        parameters = method_def[1]
        if(len(parameters) != len(arguments)):
            self.itp.error(ErrorType.TYPE_ERROR, f"You passed in {len(arguments)} argument(s) for {len(parameters)} parameter(s).")

        # TODO: Check for duplicate parameter names. Is this an error I should be checking?? Can't find it on spec.
        unique_param_names = set()
        for param in parameters:
            if param[1] in unique_param_names:
                self.itp.error(ErrorType.NAME_ERROR, f"Duplicate formal parameter name '{param[1]}'.")
            else:
                unique_param_names.add(param[1])

        # Arguments can be constants, variables, or expressions. Process them with parent's scope before creating new lexical environment.
        eval_args = []
        for arg in arguments:
            eval_args.append(self.__evaluate_expression(arg, parent_scope_vars))

        # Map parameters to arguments; add them to dictionary of visible variables (in-scope) for method call (make lex enviro)
        # Fields are always in-scope, unless shadowed.
        if(target_object_name == self.itp.ME_DEF):
            call_scope_vars = self.my_fields
        else:
            call_scope_vars = target_object.my_fields

        # Initialize and add parameters to in-scope variables. Accounts for parameters shadowing fields. 
        # I think the parameter names are shared across all objects of same class,
        # but this key is creating a new pool of visible variables for each method call, so PBV should still hold. 

        # MARK
        # Create value_def object for each value processed by evaluated expression.
        obj_args = []
        for arg in eval_args:
            obj_args.append(create_value_object(arg))
            
        # Append value_def object IFF its type matches parameter type. Otherwise, raise error.
        for i in range(len(parameters)):
            param_type = parameters[i][0]
            param_name = parameters[i][1]

            param_var = create_var_object(param_type, param_name)
            param_var_type = param_var.get_type()

            arg_val = obj_args[i].get_value()
            arg_type = obj_args[i].get_type()

            # TYPE CHECKING PARAMETER INITIALIZATION / TYPE CHECKING ASSIGNMENTS:
            # TODO: This does not account for polymorphism yet.
            if(arg_type != param_var_type):
                self.itp.error(ErrorType.NAME_ERROR, f"Parameter of type '{param_var_type}' cannot be assigned to a value of type '{arg_type}'.")
            elif(arg_type == InterpreterBase.CLASS_DEF and arg_val != InterpreterBase.NULL_DEF):
                print("CHECK FOR POLYMORPHISM HERE.")
            # Otherwise, value is primitive or null. Null can be assigned to any variables holding any type of object reference.
            else:
                call_scope_vars[param_name] = (param_var, obj_args[i])

        
        # CREATE LEXICAL ENVIRONMENT: START WITH STACK CONTAINING DICTIONARY CONTAINING FIELDS & PARAMS
        in_scope_vars = [call_scope_vars]

        # print("visible vars: ")
        # for k,v in call_scope_vars.items():
        #     print(k ,":", (v[0].get_type(), v[0].get_name()), "=", (v[1].get_type(), v[1].get_value()))

        top_level_statement = self.get_top_level_statement(method_def)
        
        # HANDLE TERMINATION
        # MARK
        # Set up default return tuples.
        return_type = method_def[0]
        if(return_type == InterpreterBase.INT_DEF):
            default_returned_val = ('0', True)
        elif(return_type == InterpreterBase.BOOL_DEF):
            default_returned_val = (InterpreterBase.FALSE_DEF, True)
        elif(return_type == InterpreterBase.STRING_DEF):
            default_returned_val = ('', True)
        # void functions return nothing (None)
        elif(return_type == InterpreterBase.VOID_DEF):
            default_returned_val = (None, True)
        # otherwise, return type is a class
        else:
            default_returned_val = (InterpreterBase.NULL_DEF, True)

        # store possible return value
        returned_val = (None, False)
        if(top_level_statement[0]==self.itp.RETURN_DEF):
            returned_val = self.__run_statement(top_level_statement[0:len(top_level_statement[0])], in_scope_vars)
        else:
            returned_val = self.__run_statement(top_level_statement, in_scope_vars)

        # either return returned_val or default_returned_val
        # if non-void functions:
        if(return_type != InterpreterBase.VOID_DEF):
            # do not run return statement or do not return a value (no return expression):
            if(returned_val[1] == False or returned_val[0] == None):
                return default_returned_val
            # does return a value --> check compatible type
            else:
                val = create_value_object(returned_val[0])
                val_type = val.get_type()

                # if return value is an object reference or null:
                if(val_type == InterpreterBase.CLASS_DEF):
                    if(val == InterpreterBase.NULL_DEF):
                        return (val.get_value(), True)
                    else:
                        print("Handle polymorphism here.")
                # else return value is a primitve 
                else:
                    # if primitive types don't match, output error
                    if(val_type != return_type):
                        self.itp.error(ErrorType.TYPE_ERROR, f"Function with return type '{return_type}' cannot return values of type '{val_type}'.")
                    else:
                        return (val.get_value(), True)
        # void function should not return value
        else:
            if(returned_val[0] != None):
                self.itp.error(ErrorType.TYPE_ERROR, "Void functions should not return any values.")
            else:
                return default_returned_val                 # set up to be (None, True) if function is void-type

    def __execute_let_statement(self, statement, in_scope_vars):            # ['let', [[type_name, var_name, init_val], [], ..], [statements]]
        local_vars = statement[0]
        substatements = statement[1:]

        local_dict = {}                             # [ 'var_name' : (var_def obj, val_def obj) ]
        for loc in local_vars:
            type_name = loc[0]
            var_name = loc[1]
            init_val = loc[2]

            if (var_name in local_dict):
                self.itp.error(ErrorType.NAME_ERROR, "No duplicate named local variables.")
            else:
                # TODO: TYPE CHECKING ASSIGNMENTS:
                var = create_var_object(type_name, var_name)
                val = create_value_object(init_val)

                var_type = var.get_type()
                val_type = val.get_type()

                # TODO: Need to handle polymorphism.
                if(val_type != var_type):
                    self.itp.error(ErrorType.TYPE_ERROR, f"Variable holds values of type '{var_type}', but value is of type '{val_type}'.")
                elif(val_type == InterpreterBase.CLASS_DEF and val != InterpreterBase.NULL_DEF):
                    print("CHECK FOR POLYMORPHISM HERE.")
                    # return
                # Otherwise, value is primitive or null. Null can be assigned to any variables holding any type of object reference.
                else:
                    # if it type checking passes, update the variable & return from function (don't run error statement)
                    local_dict[var_name] = (var, val)
                    # print(var.get_type(), var.get_name(), "==>", val.get_type(), val.get_value())

        # add this dictionary to in_scope_vars
        # does not modify original dictionary in outer 'let' statements
        # so, once we return to outer 'let' statements, their pool of variables would not have this newly appended dict
        in_scope_vars = in_scope_vars + [local_dict]

        # run the substatements with this pool of variables (similar to begin statement)
        # initially returned_val[1] == False since we just started the 'let' statement (no return statement could have ran)
        returned_val = (None, False)

        for sub in substatements:
            # HANDLE TERMINATION
            if(sub[0]==self.itp.RETURN_DEF):
                # runs return statement; returns (None or value, True)
                return self.__run_statement(sub[0:len(sub[0])], in_scope_vars)
            
            # returned_val[1] is set to True if inner statements ran a return statement
            if(returned_val[1]==False):
                returned_val = self.__run_statement(sub, in_scope_vars)

            # no more statements should be ran since inner scope terminated 
            else:
                break

        # if a nested return statement ran, propagates returned_val tuple up
        # else, returns (None, False) for sure since no return statement ran
        return returned_val
