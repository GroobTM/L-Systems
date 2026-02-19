import matplotlib.pyplot as plt
import numpy as np

from matplotlib.collections import LineCollection
from math import sin, cos, radians

from Stack import Stack

class MPLTurtle:
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__angle = 0
        self.__stack = Stack()
        self.__lines = []

        self.__sin = 0.0
        self.__cos = 1.0

    def __addLine(self, curX: float, curY: float, nextX: float, nextY: float):
        line = [(curX, curY), (nextX, nextY)]
        self.__lines.append(line)        

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
        self.__angle = transfrom[2]

    def draw(self):
        linesToDraw = LineCollection(self.__lines)

        fig, ax = plt.subplots()
        ax.add_collection(linesToDraw)
        ax.autoscale()

        plt.show()