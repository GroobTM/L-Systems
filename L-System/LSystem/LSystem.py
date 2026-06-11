from random import choice

from MyTurtle.MyTurtle import MyTurtle

class LSystem:
    def __init__(self, alphabet: dict, axiom: str, productionRules: dict):
        self.__alphabet = alphabet
        self.__axiom = axiom
        self.__productionRules = productionRules

        self.__currentGeneration = axiom
        self.__generationCount = 0

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


    def executeCurrentGeneration(self, turtle: MyTurtle, forwardCharacters: list[str]):
        noLines = 0 
        for character in forwardCharacters:
            noLines += self.__currentGeneration.count(character)
        turtle.initLineArray(noLines)

        for character in self.__currentGeneration:
            func = self.__alphabet[character]

            if (func != None):
                func.execute()

    def getCurrentGeneration(self) -> str:
        return self.__currentGeneration
    
    def getCurrentGenerationCount(self) -> int:
        return self.__generationCount