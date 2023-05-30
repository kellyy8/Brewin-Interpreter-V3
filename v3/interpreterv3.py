from classv2 import ClassDef
from intbase import InterpreterBase, ErrorType
from bparser import BParser
from objectv2 import ObjectDef
from type_valuev2 import TypeManager

# need to document that each class has at least one method guaranteed

# Main interpreter class
class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.trace_output = trace_output

    # run a program, provided in an array of strings, one string per line of source code
    # usese the provided BParser class found in parser.py to parse the program into lists
    def run(self, program):
        status, parsed_program = BParser.parse(program)
        if not status:
            super().error(
                ErrorType.SYNTAX_ERROR, f"Parse error on program: {parsed_program}"
            )
        self.__add_all_class_types_to_type_manager(parsed_program)
        self.__map_class_names_to_class_defs(parsed_program)

        # instantiate main class
        invalid_line_num_of_caller = None
        self.main_object = self.instantiate(
            InterpreterBase.MAIN_CLASS_DEF, invalid_line_num_of_caller
        )

        # call main function in main class; return value is ignored from main
        self.main_object.call_method(
            InterpreterBase.MAIN_FUNC_DEF, [], False, invalid_line_num_of_caller
        )

        # program terminates!

    # user passes in the line number of the statement that performed the new command so we can generate an error
    # if the user tries to new an class name that does not exist. This will report the line number of the statement
    # with the new command

    # PARAMETERIZED TYPES CAN BE CREATED HERE! -- object instantations
    def instantiate(self, class_name, line_num_of_statement):
        # create parameterized type if needed:
        if self.is_parameterized_type(class_name):
            self.create_parameterized_type(class_name)
        
        if class_name not in self.class_index:
            super().error(
                ErrorType.TYPE_ERROR,
                f"No class named {class_name} found",
                line_num_of_statement,
            )
        class_def = self.class_index[class_name]
        obj = ObjectDef(
            self, class_def, None, self.trace_output
        )  # Create an object based on this class definition
        return obj

    # returns a ClassDef object
    def get_class_def(self, class_name, line_number_of_statement):
        if class_name not in self.class_index:
            super().error(
                ErrorType.TYPE_ERROR,
                f"No class named {class_name} found",
                line_number_of_statement,
            )
        return self.class_index[class_name]

    # returns a bool
    def is_valid_type(self, typename):
        return self.type_manager.is_valid_type(typename)

    # returns a bool
    def is_a_subtype(self, suspected_supertype, suspected_subtype):
        return self.type_manager.is_a_subtype(suspected_supertype, suspected_subtype)

    # typea and typeb are Type objects; returns true if the two type are compatible
    # for assignments typea is the type of the left-hand-side variable, and typeb is the type of the
    # right-hand-side variable, e.g., (set person_obj_ref (new teacher))
    def check_type_compatibility(self, typea, typeb, for_assignment=False):
        return self.type_manager.check_type_compatibility(typea, typeb, for_assignment)

    def __map_class_names_to_class_defs(self, program):
        self.class_index = {}
        self.tclass_index = {}
        for item in program:
            # regular class (original code)
            if item[0] == InterpreterBase.CLASS_DEF:
                if item[1] in self.class_index:
                    super().error(ErrorType.TYPE_ERROR, f"Duplicate class name {item[1]}", item[0].line_num)
                self.class_index[item[1]] = ClassDef(item, self)
                # print(item)
            # templated class (new code)
            # [tclass temp_class_name (parameterized_type1 parameterized_type2 ...) ... ]
            elif item[0] == InterpreterBase.TEMPLATE_CLASS_DEF:
                tclass_name = item[1]
                # cannot have templated classes of the same name, despite having diff number of parameterized types
                if item[1] in self.tclass_index:
                    super().error(ErrorType.TYPE_ERROR, f"Duplicate class name {item[1]}", item[0].line_num)
                # use to define new parametrized class types as needed (runtime)
                # tclass_index = {tclass_name: [[parameterized_type1 parameterized_type2 ...], [fields], [methods]]}
                self.tclass_index[tclass_name] = item[2:]

        # print("tclasses:")
        # for k,v in self.tclass_index.items():
        #     print("tclass:")
        #     print("name:", k)
        #     print("def:", v)

    # [class classname inherits superclassname [items]]
    def __add_all_class_types_to_type_manager(self, parsed_program):
        self.type_manager = TypeManager()
        for item in parsed_program:
            # regular class (original code)
            if item[0] == InterpreterBase.CLASS_DEF:
                class_name = item[1]
                superclass_name = None
                if item[2] == InterpreterBase.INHERITS_DEF:
                    superclass_name = item[3]
                self.type_manager.add_class_type(class_name, superclass_name)

    # I added pretty much everything below this line. ----------------------------------------------

    # type_name = string; call create_parameterized type if type_name is a tclass
    def is_parameterized_type(self, type_name):
        if '@' in type_name:
            return True
        else:
            return False

    # return the type to fill in parameterized type
    def __get_type_to_assign_ptype_with(self, ptypes_passed_in, all_ptypes_to_assign, ptype_to_assign):
        i = all_ptypes_to_assign.index(ptype_to_assign)
        return ptypes_passed_in[i]

    # tclass = 'tclass_name@ptype1@ptype2...'
    def create_parameterized_type(self, tclass_str, line_num_of_statement=-1):
        # check if parameterized type exists already
        if self.is_valid_type(tclass_str):
            return

        tclass_list = tclass_str.split("@")
        tclass_name = tclass_list[0]
        ptypes_passed_in = tclass_list[1:]

        # check for invalid parameterized types: "one that is not a valid built-in type or a previously-defined class type" (from spec)
        for pt in ptypes_passed_in:
            if not self.is_valid_type(pt):
                super().error(ErrorType.TYPE_ERROR, f"{pt} is not a built-in type or previously-defined class type.", line_num_of_statement)

        # check if template exists
        if tclass_name not in self.tclass_index:
            super().error(ErrorType.TYPE_ERROR, f"No template class with the name '{tclass_name}'.", line_num_of_statement)
        # "attempt to use a templated class to define a type without fully specifying all type parameters" (from spec)
        elif len(ptypes_passed_in) != len(self.tclass_index[tclass_name][0]):
            super().error(ErrorType.TYPE_ERROR, f"Specified {len(ptypes_passed_in)} parameterized types when {len(self.tclass_index[tclass_name][1])} are requested.", line_num_of_statement)
        # build NEW parameterized type
        else:
            # retrieve the template's definition stored in interpreter's tclass_index dictionary
            tclass_stored = self.tclass_index[tclass_name]
            ptypes_to_assign = []
            for pt in tclass_stored[0]:
                ptypes_to_assign.append(pt)

            # when template class uses itself as a type in its definition, assign it with new parameterized type
            tclass_str_to_assign = tclass_name
            for pt in ptypes_to_assign:
                tclass_str_to_assign += '@' + pt
            
            ptypes_to_assign.append(tclass_str_to_assign)
            ptypes_passed_in.append(tclass_str)

            # template class's fields and methods; must update with passed in types
            tclass_def = tclass_stored[1:]

            # used later to create ClassDef object that will be added to dictionary mapping class_names to ClassDef objects
            class_def = ['class', tclass_str]

            for item in tclass_def:
                if item[0] == InterpreterBase.FIELD_DEF:
                    field_def = []
                    for i in item:
                        field_def.append(i)

                    field_type = field_def[1]

                    # TODO: Can parameterized types have the same name?
                    # check if field type is parameterized type
                    if field_type in ptypes_to_assign:
                        assigned_type = self.__get_type_to_assign_ptype_with(ptypes_passed_in, ptypes_to_assign, field_type)
                        field_def[1] = assigned_type             # only changes elements in field_def
                    
                    class_def.append(field_def)
                    # print("FD", field_def)

                elif item[0] == InterpreterBase.METHOD_DEF:
                    method_def = []
                    for i in item[0:3]:
                        method_def.append(i)
                    
                    return_type = method_def[1]

                    # check if return type is parameterized type
                    if return_type in ptypes_to_assign:
                        method_def[1] = self.__get_type_to_assign_ptype_with(ptypes_passed_in, ptypes_to_assign, return_type)

                    # print(method_def)
                    # print(item)
                    filled_out_method_body = self.__return_filled_out_thing(item[3:], ptypes_passed_in, ptypes_to_assign)
                    for b in filled_out_method_body[0]:             # actual body nested in a list; extra pair of brackets; TODO: Check if this is an error.
                        method_def.append(b)
                    class_def.append(method_def)
        
                    # print("MD", method_def)

            # add parameterized class type to list of valid class types
            self.type_manager.add_class_type(tclass_str, None)
            # add its definition to dictionary of classes -> ClassDef's
            self.class_index[tclass_str] = ClassDef(class_def, self)

    # Use recursion to traverse all lists and nested lists; update elements that are ptypes to be assigned.
    # Don't worry about variables that use another parameterized type. We are just making the method_def list.
    def __return_filled_out_thing(self, things, ptypes_passed_in, all_ptypes_to_assign):
        filled_out_things = []
        for thing in things:
            if type(thing) == list:
                filled_out_things += self.__return_filled_out_thing(thing, ptypes_passed_in, all_ptypes_to_assign)
            else:
                # TODO: only handle own templates' parameterized types. Check if logic is correct.
                if thing not in all_ptypes_to_assign:
                    filled_out_things.append(thing)
                else:
                    # if self.is_parameterized_type(t):
                    #     self.create_parameterized_type(t)
                    assigned_type = self.__get_type_to_assign_ptype_with(ptypes_passed_in, all_ptypes_to_assign, thing)
                    filled_out_things.append(assigned_type)

        return [filled_out_things]


# filename = "/Users/kellyyu/Downloads/23SP/CS131/Projects/spring-23-autograder/brew#.txt"
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