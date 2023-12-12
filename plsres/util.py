class Attributes (dict):
    def __getattr__(self, attribute):
        return self.__getitem__(attribute)

    def __setattr__(self, attribute, value):
        return self.__setitem__(attribute, value)
