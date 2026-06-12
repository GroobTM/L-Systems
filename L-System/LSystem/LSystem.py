from random import choice

from MyTurtle.MyTurtle import MyTurtle

class LSystem:
    def __init__(self, alphabet: dict, axiom: str, productionRules: dict, forwardAlphabet: list[str]):
        self.__alphabet = alphabet
        self.__axiom = axiom
        self.__productionRules = productionRules
        self.__forwardAlphabet = forwardAlphabet

        self.__currentGeneration = axiom
        self.__generationCount = 0
        self.__countLines()

    def __countLines(self):
        self.__currentLineCount = 0
        for character in self.__forwardAlphabet:
            self.__currentLineCount += self.__currentGeneration.count(character)

    def createNextGeneration(self):
        nextGeneration = []

        for character in self.__currentGeneration:
            rules = self.__productionRules.get(character, character)
            noRules = len(rules)
            if (rules == character or noRules == 0):
                nextGeneration.append(rules[0])
            else:
                nextGeneration.append(choice(rules))

        self.__currentGeneration = "".join(nextGeneration)
        self.__generationCount += 1

        self.__countLines()

    def createNthGeneration(self, n: int):
        if (n == self.__generationCount):
            return
        elif (n > self.__generationCount):
            n -= self.__generationCount
        else:
            self.__generationCount = 0
            self.__currentGeneration = self.__axiom
        
        for i in range(n):
            self.createNextGeneration()


    def executeCurrentGeneration(self, turtle: MyTurtle):
        turtle.initLineArray(self.__currentLineCount)

        for character in self.__currentGeneration:
            func = self.__alphabet[character]

            if (func != None):
                func.execute()

    def getCurrentGeneration(self) -> str:
        return self.__currentGeneration
    
    def getCurrentGenerationCount(self) -> int:
        return self.__generationCount
    
    def getCurrentGenerationLineCount(self) -> int:
        return self.__currentLineCount