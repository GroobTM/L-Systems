from random import seed

from .AlphabetFunction import AlphabetFunction
from .AlphabetOption import AlphabetOption
from .LSystem import LSystem
from MyTurtle.ImGuiTurtle import ImGuiTurtle

# TODO Add seed set
# TODO Add check for alphabet and axiom/rule compatibility
# TODO Add getter/setters for production rules
# TODO Add return to default method

class LSystemController:
    def __init__(self):
        self.__turtle = ImGuiTurtle()

        self.__alphabetOptions = {
            AlphabetOption.FORWARD : AlphabetFunction(self.__turtle.moveForward, (10, 10)),
            AlphabetOption.LEFT    : AlphabetFunction(self.__turtle.turnLeft, (30, 30)),
            AlphabetOption.RIGHT   : AlphabetFunction(self.__turtle.turnRight, (30, 30)),
            AlphabetOption.PUSH    : AlphabetFunction(self.__turtle.pushState),
            AlphabetOption.POP     : AlphabetFunction(self.__turtle.popState),
            AlphabetOption.STOP    : AlphabetFunction(None)
        }

        self.__defaultAlphabet = {
            "F" : self.__alphabetOptions[AlphabetOption.FORWARD].useFunction(),
            "+" : self.__alphabetOptions[AlphabetOption.LEFT].useFunction(),
            "-" : self.__alphabetOptions[AlphabetOption.RIGHT].useFunction(),
            "[" : self.__alphabetOptions[AlphabetOption.PUSH].useFunction(),
            "]" : self.__alphabetOptions[AlphabetOption.POP].useFunction(),
            "X" : self.__alphabetOptions[AlphabetOption.STOP].useFunction()
        }
        self.__alphabet = self.__defaultAlphabet.copy()

        self.__defaultForwardAlphabet = ["F"]
        self.__forwardAlphabet = self.__defaultForwardAlphabet.copy()

        self.__defaultProductionRules = {
            "X": "F[+X][-X]FX",
            "F": "FF"
        }
        self.__productionRules = self.__defaultProductionRules.copy()

        self.__defaultAxiom = "X"
        self.__axiom = self.__defaultAxiom

        self.__seed = -1

        self.resetLSystem()

    def resetLSystem(self):
        self.__lSystem = LSystem(self.__alphabet.copy(), self.__axiom, self.__productionRules.copy())

    def resetGeneration(self):
        self.__lSystem.createNthGeneration(0)
        self.__lSystem.executeCurrentGeneration(self.__turtle, self.__forwardAlphabet)
        self.__turtle.resetCanvas()

    def generateNextGeneration(self):
        self.__lSystem.createNextGeneration()
        self.__lSystem.executeCurrentGeneration(self.__turtle, self.__forwardAlphabet)
        self.__turtle.resetCanvas()

    def getCurrentGeneration(self) -> str:
        return self.__lSystem.getCurrentGeneration()
    
    def getCurrentGenerationCount(self) -> int:
        return self.__lSystem.getCurrentGenerationCount()
    
    def drawLSystem(self):
        self.__turtle.draw()

    def getAlphabetOptions(self) -> dict:
        return self.__alphabetOptions
    
    def getAlphabet(self) -> dict:
        return self.__alphabet
    
    def addToAlphabet(self, character : str, option : AlphabetOption, value : tuple[float, float] = None):
        if (character.count() != 1):
            raise RuntimeError(character + " is not 1 character.")
        
        self.__alphabet[character] = self.__alphabetOptions[option].useFunction(value)

        if (option.value == AlphabetOption.FORWARD):
            self.__forwardAlphabet.append(character)

    def removeFromAlphabet(self, character : str):
        if (character in self.__alphabet):
            self.__alphabet.pop(character)

        if (character in self.__forwardAlphabet):
            self.__forwardAlphabet.pop(character)

    def getAxiom(self) -> str:
        return self.__axiom
    
    def setAxiom(self, axiom: str):
        self.__axiom = axiom