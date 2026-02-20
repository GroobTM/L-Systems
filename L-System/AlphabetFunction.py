class AlphabetFunction:
    def __init__(self, function, value = None):
        self.__function = function
        self.__value = value
    
    def execute(self):
        if (self.__value == None):
            self.__function()
        else:
            self.__function(self.__value)