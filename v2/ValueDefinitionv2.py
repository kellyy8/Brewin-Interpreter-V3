class ValueDefinition:
    # store 'value' objects and their type
    def __init__(self, val_type, val, class_name=None):
        # can be primitives (int, string, bool) or class types (class name)
        self.type = val_type
        self.value = val
        self.class_name = class_name

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def get_class_name(self):
        return self.class_name