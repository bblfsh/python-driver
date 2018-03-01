class cls1:
    def __init__(self): self.__x = 0

    @property
    def x(self): return self.__x

    @x.setter
    def x(self, value): self.__x = value
