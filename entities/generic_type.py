class GenericType(object):

    def __init__(self, type_id, name, note, required):
        self.__type_id = type_id
        self.__name = name
        self.__note = note
        self.__required = required

    def get_id(self):
        return self.__type_id

    def get_name(self):
        return self.__name

    def get_note(self):
        return self.__note

    def is_required_(self):
        return self.__required