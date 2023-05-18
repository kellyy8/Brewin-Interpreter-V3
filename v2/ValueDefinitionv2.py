from intbase import InterpreterBase

class ValueDefinition:
    def __init__(self, val, val_type, class_name=None):
        self.value = val
        self.type = val_type
        # for object references that are not null
        self.class_name = class_name

        # TODO: CHECK IF THESE TYPE TRANSLATIONS ARE EXHUASTIVE AND CORRECT.
        # # I think every other object would be parsed as a string value except for objects.
        # # Must check for objects first because other if statements iterate val to type check.
        # # print(type(val)) # == <class 'bparser.StringWithLineNumber'>
        # # print(str)
        # # if (type(val) != str):
        # #     self.type = val.get_object_type()
        # if val[0] == '"':
        #     self.type = InterpreterBase.STRING_DEF
        # elif val == InterpreterBase.TRUE_DEF or val == InterpreterBase.FALSE_DEF:
        #     self.type = InterpreterBase.BOOL_DEF
        # elif val == InterpreterBase.NULL_DEF:
        #     self.type = InterpreterBase.CLASS_DEF
        # else:
        #     self.type = InterpreterBase.INT_DEF

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def get_class_name(self):
        return self.class_name