from intbase import InterpreterBase, ErrorType
from ValueDefinitionv2 import ValueDefinition

# parser:
# [ 'field', 'type_name', 'field_name', 'init_value']
# [ 'method', 'return_type', 'name', [[type1, param1], [type2, param2], ..], ['top-level statement'] ]

# When assigning a value to a variable (field init, param init, reassignment), use a value_def object as the value to work with.
def create_value_def_object(val, class_name=None):
    if (type(val) == ObjectDefinition):
        return ValueDefinition(val, InterpreterBase.CLASS_DEF, val.get_object_type())
    elif val[0] == '"':
        return ValueDefinition(val, InterpreterBase.STRING_DEF, None)
    elif val == InterpreterBase.TRUE_DEF or val == InterpreterBase.FALSE_DEF:
        return ValueDefinition(val, InterpreterBase.BOOL_DEF, None)
    elif val == InterpreterBase.NULL_DEF:
        return ValueDefinition(val, InterpreterBase.CLASS_DEF, class_name)
    else:
        return ValueDefinition(val, InterpreterBase.INT_DEF, None)
    
class ObjectDefinition:
    def __init__(self, interpreter, class_name, class_def):
        self.class_name = class_name
        self.my_methods = {}                                   #{ 'method_name' : 'return_type', [[type1, param1], [type2, param2], ..], ['top-level statement'] }
        self.my_fields = {}                                    #{ 'field_name' : value_def object }
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
                    # TYPE CHECKING FIELD INITIALIZATION: create value object & retrieve its type; store object IFF its type matches field's type
                    # If val == 'null', val can only be updated to point object references of variable's 'type_name'
                    if(init_val == InterpreterBase.NULL_DEF):
                        init_val = create_value_def_object(init_val, type_name)
                    else:
                        init_val = create_value_def_object(init_val)
                    
                    init_val_type = init_val.get_type()
                    #TODO: This does not account for polymorphism yet. Not yet comparing class names if type == CLASS_DEF 
                    if(init_val_type != type_name):
                        self.itp.error(ErrorType.TYPE_ERROR, f"Field of type '{type_name}' cannot be initialized with a value of type '{init_val_type}'.")
                    else:
                        self.my_fields[field_name] = init_val
            
            elif item[0] == self.itp.METHOD_DEF:
                method_name = item[2]
                if(method_name in self.my_methods):
                    self.itp.error(ErrorType.NAME_ERROR, "Methods cannot share the same name.")
                # map method name to its whole definition (return, params, statements)
                else:
                    # TODO: Update to BREWIN++ version later.
                    self.my_methods[method_name] = [item[1]] + item[3:]   # BREWIN++ version
                    # self.my_methods[method_name] = item[3:]                 # BREWIN version

        # for name, val in self.my_fields.items():
        #     print(val.get_type(), name, "=", val.get_value())
        # print(self.my_methods)

    def get_object_type(self):
        return self.class_name

    # JUST FOR MAIN() IN MAIN CLASS.
    def call_main_method(self, method_name):
        method_def = self.__find_method(method_name)
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
        # in_scope_vars = self.my_fields by default --> arg passed in if there are params in addition to fields that are visible
        # MARK
        if(in_scope_vars is None):
            in_scope_vars = self.my_fields
        
        # ('return value', termination indicator) ('return value' extracted in 'call expressions')
        # MARK - RETURNED_VAL
        returned_val = ('', False)
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
                returned_val = ('', True)
        elif statement[0] == self.itp.BEGIN_DEF:
            returned_val = self.__execute_all_sub_statements_of_begin_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.SET_DEF:
            self.__execute_set_statement(statement[1:], in_scope_vars)
        elif statement[0] == self.itp.CALL_DEF:
            returned_val = self.__execute_call_statement(statement[1:], in_scope_vars)

        return returned_val
    
    def __get_const_or_var_val(self, expr, in_scope_vars):
        # MARK -- DEPENDS ON HOW EXPR IS PASSED IN OMG
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

            # class_obj = ClassDefinition(expression[1], class_def, self.itp)
            # instance = class_obj.instantiate_object()
            # return instance

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
    # TODO: Store value_def objects rather than values into variables. (Do we have to check the variable's type matches int/str?)
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

        # condition is not a boolean
        if(condition_result != self.itp.TRUE_DEF and condition_result != self.itp.FALSE_DEF):
            self.itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        # condition passes
        elif(condition_result == self.itp.TRUE_DEF):
            if_body = statement[1]
            # HANDLE TERMINATION
            if(if_body[0]==self.itp.RETURN_DEF):
                # runs return statement; returns ('' or value, True)
                return self.__run_statement(if_body[0:len(if_body[0])], in_scope_vars)
            else:
                # propagates returned_val tuple up
                return self.__run_statement(if_body, in_scope_vars)
        # condition fails and there's an else-body
        elif (len(statement)==3):
            else_body = statement[2]
            # HANDLE TERMINATION
            if(else_body[0]==self.itp.RETURN_DEF):
                # runs return statement; returns ('' or value, True)
                return self.__run_statement(else_body[0:len(else_body[0])], in_scope_vars)
            else:
                # propagates returned_val tuple up
                return self.__run_statement(else_body, in_scope_vars)
        # condition fails and there's NO else-body
        else:
            # return empty string (aka nothing); if no if/else body ran, no return statement would have ran & no value returned
            returned_val = ('', False)
            return returned_val

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
                    # runs return statement; returns ('' or value, True); terminates while loop
                    return self.__run_statement(statement[1][0:len(statement[1])], in_scope_vars)

                # propagates returned_val tuple up (after while loop is done)
                returned_val = self.__run_statement(statement[1], in_scope_vars)
                condition_result = self.__evaluate_expression(statement[0], in_scope_vars)

                # another check --> since we run and use the condition again
                if(condition_result != self.itp.TRUE_DEF and condition_result != self.itp.FALSE_DEF):
                    self.itp.error(ErrorType.TYPE_ERROR, "Condition of the if statement must evaluate to a boolean type.")
        
        # if while loop ran, propagates (possibly updated) returned_val tuple up
        # else, the while loop returns ('', False) for sure since no return statement ran
        return returned_val

    def __execute_return_statement(self, statement, in_scope_vars):            # [return] or [return, [expression]]
        # HANDLE TERMINATION
        return (self.__evaluate_expression(statement, in_scope_vars), True)

    def __execute_all_sub_statements_of_begin_statement(self, statement, in_scope_vars):
        # initially returned_val[1] == False since we just entered the begin statement (no return statement could have ran)
        returned_val = ('', False)

        for substatement in statement:
            # HANDLE TERMINATION
            if(substatement[0]==self.itp.RETURN_DEF):
                # runs return statement; returns ('' or value, True)
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
        # else, returns ('', False) for sure since no return statement ran
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

        # method_def == ['return_type', [[type1, param1], [type2, param2], ..], ['top-level statement']]

        # Check if number of arguments matches number of parameters.
        parameters = method_def[1]
        if(len(parameters) != len(arguments)):
            self.itp.error(ErrorType.TYPE_ERROR, f"You passed in {len(arguments)} argument(s) for {len(parameters)} parameter(s).")

        # Arguments can be constants, variables, or expressions. Process them with parent's scope before creating new lexical environment.
        eval_args = []
        for arg in arguments:
            eval_args.append(self.__evaluate_expression(arg, parent_scope_vars))

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

        # MARK
        # Create value_def object for each value processed by evaluated expression.
        for i in range(len(eval_args)):
            eval_args[i] = create_value_def_object(eval_args[i])

        # Append value_def object IFF its type matches parameter type. Otherwise, raise error.
        for i in range(len(parameters)):
            param_type = parameters[i][0]
            param_name = parameters[i][1]
            arg_type = eval_args[i].get_type()
            # TODO: This does not account for polymorphism yet.
            # If param_type is not int, string, or bool, then it is a 'class name'. (CLASS_DEF)
            # Handle int, string, bool param types:
            if(param_type == InterpreterBase.INT_DEF or param_type == InterpreterBase.STRING_DEF or param_type == InterpreterBase.BOOL_DEF):
                if(arg_type != param_type):
                    self.itp.error(ErrorType.NAME_ERROR, f"Parameter of type '{param_type}' cannot be assigned to a value of type '{arg_type}'.")
                else:
                    visible_vars[param_name] = eval_args[i]
            # Handle class types: (TODO: handle polymorphism here)
            # else:

        # for k,v in visible_vars.items():
        #     print(k,":", v.get_type(), v.get_value())

        top_level_statement = self.get_top_level_statement(method_def)
        
        # HANDLE TERMINATION
        # MARK
        # Check first value of tuple (value def object) and see if its type matches return type.
        if(top_level_statement[0]==self.itp.RETURN_DEF):
            return self.__run_statement(top_level_statement[0:len(top_level_statement[0])], visible_vars)
        return self.__run_statement(top_level_statement, visible_vars)
