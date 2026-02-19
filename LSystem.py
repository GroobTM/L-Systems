from MyTurtle import MyTurtle
from MPLTurtle import MPLTurtle
from Stack import Stack
from ProductionRule import ProductionRule
from AlphabetFunction import AlphabetFunction

class LSystem:
    def __init__(self, alphabet: dict, axiom: str, productionRules: list):
        self.__alphabet = alphabet
        self.__axiom = axiom
        self.__productionRules = productionRules

        self.__currentGeneration = axiom
        self.__generationCount = 0

    def createNextGeneration(self):
        nextGeneration = ""

        for character in self.__currentGeneration:
            ruleExists = False

            for rule in self.__productionRules:
                if (rule.matchesInitialPattern(character)):
                    ruleExists = True
                    nextGeneration += rule.finalPattern
                    break

            if (not ruleExists):
                nextGeneration += character

        self.__currentGeneration = nextGeneration
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

productionRules = [
    ProductionRule("X", "F[+X][-X]FX"),
    ProductionRule("F", "FF")
]



lSystem = LSystem(alphabet, "X", productionRules)

lSystem.createNthGeneration(14)
lSystem.executeCurrentGeneration()

t.draw()
