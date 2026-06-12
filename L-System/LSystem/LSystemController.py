from random import seed, randrange
from copy import deepcopy
from sys import maxsize

from .AlphabetFunction import AlphabetFunction
from .AlphabetOption import AlphabetOption
from .LSystem import LSystem
from MyTurtle.ImGuiTurtle import ImGuiTurtle

class LSystemController:
    def __init__(self):
        self.__turtle = ImGuiTurtle()

        self.__alphabetOptions = {
            AlphabetOption.FORWARD : AlphabetFunction(AlphabetOption.FORWARD, self.__turtle.moveForward, (10, 10)),
            AlphabetOption.LEFT    : AlphabetFunction(AlphabetOption.LEFT, self.__turtle.turnLeft, (30, 30)),
            AlphabetOption.RIGHT   : AlphabetFunction(AlphabetOption.RIGHT, self.__turtle.turnRight, (30, 30)),
            AlphabetOption.PUSH    : AlphabetFunction(AlphabetOption.PUSH, self.__turtle.pushState),
            AlphabetOption.POP     : AlphabetFunction(AlphabetOption.POP, self.__turtle.popState),
            AlphabetOption.STOP    : AlphabetFunction(AlphabetOption.STOP, None)
        }

        self.__defaultAlphabet = {
            "F" : self.__alphabetOptions[AlphabetOption.FORWARD].useFunction(),
            "+" : self.__alphabetOptions[AlphabetOption.LEFT].useFunction(),
            "-" : self.__alphabetOptions[AlphabetOption.RIGHT].useFunction(),
            "[" : self.__alphabetOptions[AlphabetOption.PUSH].useFunction(),
            "]" : self.__alphabetOptions[AlphabetOption.POP].useFunction(),
            "X" : self.__alphabetOptions[AlphabetOption.STOP].useFunction()
        }

        self.__defaultForwardAlphabet = ["F"]

        self.__defaultProductionRules = {
            "X": ["F[+X][-X]FX"],
            "F": ["FF"]
        }

        self.__defaultAxiom = "X"

        self.randomiseSeed()
        self.setToDefaults()
        self.resetLSystem()

    def setToDefaults(self):
        self.__alphabet = self.__defaultAlphabet.copy()
        self.__forwardAlphabet = self.__defaultForwardAlphabet.copy()
        self.__productionRules = deepcopy(self.__defaultProductionRules)
        self.__axiom = self.__defaultAxiom

    def resetLSystem(self):
        self.__lSystem = LSystem(self.__alphabet.copy(), self.__axiom, deepcopy(self.__productionRules), self.__forwardAlphabet.copy())
        self.__resetToSeed()

    def createNextGeneration(self):
        self.__lSystem.createNextGeneration()

    def createNthGeneration(self, n: int):
        if (n < self.getCurrentGenerationCount()):
            self.__resetToSeed()
        self.__lSystem.createNthGeneration(n)

    def resetGeneration(self):
        self.createNthGeneration(0)
        self.executeCurrentGeneration()

    def executeCurrentGeneration(self):
        self.__lSystem.executeCurrentGeneration(self.__turtle)
        self.__turtle.resetCanvas()

    def getCurrentGeneration(self) -> str:
        return self.__lSystem.getCurrentGeneration()
    
    def getCurrentGenerationCount(self) -> int:
        return self.__lSystem.getCurrentGenerationCount()
    
    def lineCountGTEThreshold(self, threshold: int) -> bool:
        return self.__lSystem.getCurrentGenerationLineCount() >= threshold

    def drawLSystem(self):
        self.__turtle.draw()

    ### ----- Alphabet Methods -----
    def getAlphabetOptions(self) -> dict:
        return self.__alphabetOptions
    
    def getAlphabet(self) -> dict:
        return self.__alphabet
    
    def addToAlphabet(self, character: str, option: AlphabetOption, value: tuple[float, float] = None):
        if (len(character) != 1):
            raise RuntimeError(character + " is not 1 character.")
        
        self.__alphabet[character] = self.__alphabetOptions[option].useFunction(value)

        if (option.value == AlphabetOption.FORWARD):
            self.__forwardAlphabet.append(character)

    def removeFromAlphabet(self, character: str):
        if (character in self.__alphabet):
            self.__alphabet.pop(character)

        if (character in self.__forwardAlphabet):
            self.__forwardAlphabet.remove(character)

    def isAlphabetCompatible(self) -> bool:
        compatible = True
        for character in self.__productionRules:
            compatible = compatible and character in self.__alphabet
            if (not compatible):
                return compatible
            
        for character in self.__axiom:
            compatible = compatible and character in self.__alphabet
            if (not compatible):
                return compatible
            
        return compatible

    ### ----- Axiom Methods -----
    def getAxiom(self) -> str:
        return self.__axiom
    
    def setAxiom(self, axiom: str):
        self.__axiom = axiom

    ### ----- Production Rules Methods -----
    def getProductionRules(self) -> dict:
        return self.__productionRules
    
    def addToProductionRules(self, character: str, rule: str):
        if (len(character) != 1):
            raise RuntimeError(character + " is not 1 character.")
        if (rule == None):
            raise RuntimeError("Production rule value cannot be None")
        
        if (character in self.__productionRules):
            if (rule not in self.__productionRules[character]):
                self.__productionRules[character].append(rule)
        else:
            self.__productionRules[character] = [rule]

    def removeFromProductionRules(self, character: str, rule: str):
        if (character in self.__productionRules and rule in self.__productionRules[character]):
            if (len(self.__productionRules[character]) <= 1):
                self.__productionRules.pop(character)
            else:
                self.__productionRules[character].remove(rule)

    ### ----- Seed Methods -----
    def getSeed(self) -> int:
        return self.__seed
    
    def setSeed(self, newSeed: int):
        self.__seed = newSeed
        seed(self.__seed)

    def randomiseSeed(self):
        self.setSeed(randrange(maxsize))

    def __resetToSeed(self):
        seed(self.__seed)
