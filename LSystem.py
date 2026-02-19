from MyTurtle import MyTurtle
from MPLTurtle import MPLTurtle
from Stack import Stack
from AlphabetFunction import AlphabetFunction

import time

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
            nextGeneration.append(self.__productionRules.get(character, character))

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


    def executeCurrentGeneration(self):
        for character in self.__currentGeneration:
            func = self.__alphabet[character]

            if (func != None):
                func.execute()

    def getCurrentGeneration(self) -> str:
        return self.__currentGeneration


t = MPLTurtle()

alphabet = {
    "F" : AlphabetFunction(t.moveForward, 10),
    "+" : AlphabetFunction(t.turnLeft, 30),
    "-" : AlphabetFunction(t.turnRight, 30),
    "[" : AlphabetFunction(t.pushState),
    "]" : AlphabetFunction(t.popState),
    "X" : None
}

productionRules = {
    "X": "F[+X][-X]FX",
    "F": "FF"
}



lSystem = LSystem(alphabet, "X", productionRules)

lSystem.createNthGeneration(10)
lSystem.executeCurrentGeneration()

t.draw()
