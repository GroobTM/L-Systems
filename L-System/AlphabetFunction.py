from __future__ import annotations
from random import uniform

class AlphabetFunction:
    def __init__(self, function, valueBounds : tuple[float, float] = None):
        self.__function = function
        self.__valueBounds = valueBounds
    
    def execute(self):
        if (self.__function != None):
            if (self.__valueBounds == None):
                self.__function()
            else:
                if (self.__valueBounds[0] == self.__valueBounds[1]):
                    self.__function(self.__valueBounds[0])
                else:
                    value = uniform(self.__valueBounds[0], self.__valueBounds[1])
                    self.__function(value)

    def useFunction(self, valueBounds : tuple[float, float] = None) -> AlphabetFunction:
        if ((self.__valueBounds == None or (self.__valueBounds != None and valueBounds == None))):
            return AlphabetFunction(self.__function, self.__valueBounds)
        else:
            return AlphabetFunction(self.__function, valueBounds)