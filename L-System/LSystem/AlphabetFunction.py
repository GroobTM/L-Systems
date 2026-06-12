from __future__ import annotations
from random import uniform

from .AlphabetOption import AlphabetOption

class AlphabetFunction:
    def __init__(self, alphabetOption: AlphabetOption, function, valueBounds : tuple[float, float] = None):
        self.__alphabetOption = alphabetOption
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
            return AlphabetFunction(self.__alphabetOption, self.__function, self.__valueBounds)
        else:
            return AlphabetFunction(self.__alphabetOption, self.__function, valueBounds)
        
    def getAlphabetOption(self) -> AlphabetOption:
        return self.__alphabetOption
    
    def getValue(self) -> tuple[float, float]:
        return self.__valueBounds
    
    def convertToDict(self) -> dict[str, tuple[float, float]]:
        return {
            "alphabetOption" : self.__alphabetOption,
            "value" : self.__valueBounds
        }