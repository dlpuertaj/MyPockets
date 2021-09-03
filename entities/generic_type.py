class GenericType(object):

    def __init__(self, id, name, note):
        self.__id = id
        self.__name = name
        self.__note = note

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_note(self):
        return self.__note