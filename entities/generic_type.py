class GenericType(object):

    def __init__(self, type_id, name, note):
        self.__type_id = type_id
        self.__name = name
        self.__note = note

    def get_id(self):
        return self.__type_id

    def get_name(self):
        return self.__name

    def get_note(self):
        return self.__note