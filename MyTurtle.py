from copy import copy
from math import sin, cos
from turtle import Turtle

from Transform import Transform
from Stack import Stack

class MyTurtle:
    def __init__(self):
        self.__t = Turtle()
        self.__t.hideturtle()
        self.__transform = Transform()
        self.__stack = Stack()

    def __updateTransforms(self):
        self.__transform.setPosition(self.__t.xcor(), self.__t.ycor())
        self.__transform.setAngle(self.__t.heading())

    def __setTurtleToTransform(self):
        self.hide()
        self.__transform.getPosition()

    def moveTo(self, x, y):
        self.__t.goto(x, y)
        self.__updateTransforms()

    def moveForward(self, distance: float):
        x, y = self.__transform.getPosition()
        x += distance * cos(self.__angle)
        y += distance * sin(self.__angle)
        self.moveTo(x, y)
        self.__updateTransforms()

    def setAngle(self, angle: float):
        self.__transform.setAngle(angle)
        self.__t.setheading(angle)

    def addAngle(self, angle: float):
        angle += self.__transform.getAngle()
        self.__transform.setAngle(angle)
        self.__t.setheading(angle)

    def turnLeft(self, angle: float):
        self.addAngle(angle)

    def turnRight(self, angle: float):
        self.addAngle(-angle)

    def hide(self):
        self.__t.penup()
    
    def show(self):
        self.__t.pendown()

    def loop(self):
        self.__t.screen.mainloop()

    def pushState(self):
        self.__stack.push(copy(self.__transform))

    def popState(self):
        transfrom = self.__stack.pop()
        self.__transform.setFromTransform(transfrom)