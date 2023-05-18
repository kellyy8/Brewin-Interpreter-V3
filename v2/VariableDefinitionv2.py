class VariableDefinition:
    #  assign 'variable' objects with a type
    def __init__(self, var_type, var_name, class_name=None):
        # can be primitives (int, string, bool) or class types (class name)
        self.type = var_type
        self.name = var_name
        self.class_name = class_name

    # def __eq__(self, other):
    #     if(self.type == other.get_type() and self.name == other.get_name()):
    #         return True
    #     else:
    #         return False

    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type

    def get_class_name(self):
        return self.class_name


    