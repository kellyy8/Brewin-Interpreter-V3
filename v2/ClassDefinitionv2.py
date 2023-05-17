from intbase import ErrorType
from ObjectDefinitionv2 import ObjectDefinition

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
    
