from random import seed

from AlphabetFunction import AlphabetFunction
from MyTurtle.ImGuiTurtle import ImGuiTurtle
from LSystem import LSystem

# TODO Add seed set
# TODO Add check for alphabet and axiom/rule compatibility
# TODO Add getter/setters for production rules
# TODO Add return to default method

class LSystemController:
    def __init__(self):
        self.__turtle = ImGuiTurtle()

        self.__alphabetOptions = {
            "Move forward"  : AlphabetFunction(self.__turtle.moveForward, (10, 10)),
            "Turn left"     : AlphabetFunction(self.__turtle.turnLeft, (30, 30)),
            "Turn right"    : AlphabetFunction(self.__turtle.turnRight, (30, 30)),
            "Push"          : AlphabetFunction(self.__turtle.pushState),
            "Pop"           : AlphabetFunction(self.__turtle.popState),
            "Stop"          : AlphabetFunction(None)
        }

        self.__defaultAlphabet = {
            "F" : self.__alphabetOptions["Move forward"].useFunction(),
            "+" : self.__alphabetOptions["Turn left"].useFunction(),
            "-" : self.__alphabetOptions["Turn right"].useFunction(),
            "[" : self.__alphabetOptions["Push"].useFunction(),
            "]" : self.__alphabetOptions["Pop"].useFunction(),
            "X" : self.__alphabetOptions["Stop"].useFunction()
        }
        self.__alphabet = self.__defaultAlphabet.copy()

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
        self.__lSystem.executeCurrentGeneration(self.__turtle)
        self.__turtle.resetCanvas()

    def generateNextGeneration(self):
        self.__lSystem.createNextGeneration()
        self.__lSystem.executeCurrentGeneration(self.__turtle)
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
    
    def addToAlphabet(self, letter : str, option : str, value : tuple[float, float] = None):
        if (letter.count() != 1):
            raise RuntimeError(letter + " is not 1 letter.")
        if (option not in self.__alphabetOptions):
            raise RuntimeError(option + " does not exist.")
        
        self.__alphabet[letter] = self.__alphabetOptions[option].useFunction(value)

    def removeFromAlphabet(self, letter : str):
        if (letter in self.__alphabet):
            self.__alphabet.pop(letter)

    def getAxiom(self) -> str:
        return self.__axiom
    
    def setAxiom(self, axiom: str):
        self.__axiom = axiom