import numpy as np

from abc import ABC, abstractmethod
from math import sin, cos, radians

from .Stack import Stack

class MyTurtle(ABC):
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__angle = 0
        self.__stack = Stack()
        self.__lines = None
        self.__lineCounter = 0

        self.__sin = 0.0
        self.__cos = 1.0

    def initLineArray(self, length: int):
        self.__lines = np.zeros((length, 2, 2))

    def __addLine(self, curX: float, curY: float, nextX: float, nextY: float):
        if (not isinstance(self.__lines, np.ndarray)):
            raise RuntimeError("Line array not initialised. Run initLineArray() first")
        
        self.__lines[self.__lineCounter, 0, 0] = curX
        self.__lines[self.__lineCounter, 0, 1] = curY
        self.__lines[self.__lineCounter, 1, 0] = nextX
        self.__lines[self.__lineCounter, 1, 1] = nextY

        self.__lineCounter += 1

    def setAngle(self, angle: float):
        self.__angle = angle
        self.__sin = sin(radians(angle))
        self.__cos = cos(radians(angle))

    def moveTo(self, x: float, y: float):
        self.__addLine(self.__x, self.__y, x, y)
        self.__x = x
        self.__y = y

    def moveForward(self, distance: float):
        x, y = self.__x, self.__y
        x += distance * self.__cos
        y += distance * self.__sin
        self.moveTo(x, y)

    def addAngle(self, angle: float):
        angle += self.__angle
        self.setAngle(angle)

    def turnLeft(self, angle: float):
        self.addAngle(angle)

    def turnRight(self, angle: float):
        self.addAngle(-angle)

    def pushState(self):
        self.__stack.push((self.__x, self.__y, self.__angle))

    def popState(self):
        transfrom = self.__stack.pop()
        self.__x = transfrom[0]
        self.__y = transfrom[1]
        self.setAngle(transfrom[2])

    @abstractmethod
    def draw(self):
        pass