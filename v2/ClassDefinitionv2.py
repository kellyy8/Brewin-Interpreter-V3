from intbase import ErrorType
from ObjectDefinitionv2 import ObjectDefinition
# from VariableDefinitionv2 import VariableDefinition
# from ValueDefinitionv2 import ValueDefinition

class ClassDefinition:
    def __init__(self, name, definition, interpreter):
        # store each class's name (help with type checking later?) & their methods (list) and fields (list)
        self.class_name = name
        # self.my_methods = {}
        # self.my_fields = {}
        self.itp = interpreter
        self.definition = definition

        # # similar code in ObjectDefinition to handle "new" statement
        # for item in definition:
        #     if item[0] == self.itp.FIELD_DEF:                           #{'field': ['type_name', 'field_name', 'init_value']}
        #         if(item[1] in self.my_fields):
        #             self.itp.error(ErrorType.NAME_ERROR, "Fields cannot share the same name.")
        #         self.my_fields[item[1]] = item[2:]
        #     elif item[0] == self.itp.METHOD_DEF:                        #{'method': ['return_type', 'name', [[type1, param1], [type2, param2], ..], ['top-level statement']]}
        #         if(item[1] in self.my_methods):
        #             self.itp.error(ErrorType.NAME_ERROR, "Methods cannot share the same name.")
        #         self.my_methods[item[1]] = item[2:]

    # use definition of a class to create & return an instance of object
    # TODO: Consider instantiating a Variable and Value object when creating an instance to implement PBV.
    def instantiate_object(self): 
        # PBV: create new 'object definition' object each time; each object populated with own fields and methods dict
        obj = ObjectDefinition(self.itp, self.class_name, self.definition)
        # for name, info in self.my_fields.items():
        #     type_name = info[0]
        #     field_name = info[1]
        #     init_val = info[2]

        #     var = VariableDefinition(type_name, field_name)
        #     val = ValueDefinition(type_name, init_val)
        #     obj.add_field(var, val)

        # for name, info in self.my_methods.items():
        #     return_type = info[0]
        #     name = info[1]
        #     params = info[2]
        #     statements = info[3]

        #     obj.add_method(name, definition)
        return obj     