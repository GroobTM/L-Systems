import matplotlib.pyplot as plt
import numpy as np

from copy import copy
from matplotlib.collections import LineCollection
from math import sin, cos, radians

from Transform import Transform
from Stack import Stack

class MPLTurtle:
    def __init__(self):
        self.__transform = Transform(0, 0, 0)
        self.__stack = Stack()
        self.__lines = []

    def __addLine(self, curX: float, curY: float, nextX: float, nextY: float):
        line = [(curX, curY), (nextX, nextY)]
        self.__lines.append(line)

    def __updateTransform(self, newX: float = None, newY: float = None, newAngle: float = None):
        if (newX != None and newY != None):
            self.__transform.setPosition(newX, newY)
        
        if (newAngle != None):
            self.__transform.setAngle(newAngle)

    def moveTo(self, x: float, y: float):
        oldX, oldY = self.__transform.getPosition()
        self.__addLine(oldX, oldY, x, y)
        self.__updateTransform(newX = x, newY = y)

    def moveForward(self, distance: float):
        x, y = self.__transform.getPosition()
        angle = radians(self.__transform.getAngle())
        x += distance * cos(angle)
        y += distance * sin(angle)
        self.moveTo(x, y)

    def setAngle(self, angle: float):
        self.__updateTransform(newAngle = angle)

    def addAngle(self, angle: float):
        angle += self.__transform.getAngle()
        self.setAngle(angle)

    def turnLeft(self, angle: float):
        self.addAngle(angle)

    def turnRight(self, angle: float):
        self.addAngle(-angle)

    def pushState(self):
        self.__stack.push(copy(self.__transform))

    def popState(self):
        transfrom = self.__stack.pop()
        self.__transform.setFromTransform(transfrom)

    def draw(self):
        linesToDraw = LineCollection(self.__lines)

        fig, ax = plt.subplots()
        ax.add_collection(linesToDraw)
        ax.autoscale()

        plt.show()