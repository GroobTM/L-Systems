from copy import copy
from math import sin, cos, radians
from turtle import Turtle

from Transform import Transform
from Stack import Stack

class MyTurtle:
    CANVAS_PADDING = 20

    def __init__(self):
        self.__t = Turtle()
        self.__initTurtle()        

        self.__transform = Transform(0, 0, 0)
        self.__stack = Stack()

    def __initTurtle(self):
        self.__canvasMinX = -100
        self.__canvasMaxX =  100
        self.__canvasMinY = -100
        self.__canvasMaxY =  100

        self.resizeCanvas()
        self.__t.hideturtle()
        self.__t.speed(0)
        self.__t.screen.tracer(0)
        

    def __updateTransforms(self):
        self.__transform.setPosition(self.__t.xcor(), self.__t.ycor())
        self.__transform.setAngle(self.__t.heading())

    def __updateCanvasSize(self):
        x, y = self.__transform.getPosition()

        # Suggested by Gemini 
        self.__canvasMinX = min(self.__canvasMinX, x)
        self.__canvasMaxX = max(self.__canvasMaxX, x)
        self.__canvasMinY = min(self.__canvasMinY, y)
        self.__canvasMaxY = max(self.__canvasMaxY, y)

    def __setTurtleToTransform(self):
        self.hide()
        x, y = self.__transform.getPosition()
        self.__t.goto(x, y)
        self.__t.setheading(self.__transform.getAngle())
        self.__updateTransforms()
        self.show()

    def moveTo(self, x: float, y: float):
        self.__t.goto(x, y)
        self.__updateTransforms()
        self.__updateCanvasSize()

    def moveForward(self, distance: float):
        x, y = self.__transform.getPosition()
        angle = radians(self.__transform.getAngle())
        x += distance * cos(angle)
        y += distance * sin(angle)
        self.moveTo(x, y)
        self.__updateTransforms()
        self.__updateCanvasSize()

    def setAngle(self, angle: float):
        self.__t.setheading(angle)
        self.__updateTransforms()
        self.__updateCanvasSize()

    def addAngle(self, angle: float):
        angle += self.__transform.getAngle()
        self.__t.setheading(angle)
        self.__updateTransforms()
        self.__updateCanvasSize()

    def turnLeft(self, angle: float):
        self.addAngle(angle)

    def turnRight(self, angle: float):
        self.addAngle(-angle)

    def hide(self):
        self.__t.penup()
    
    def show(self):
        self.__t.pendown()

    def pushState(self):
        self.__stack.push(copy(self.__transform))

    def popState(self):
        transfrom = self.__stack.pop()
        self.__transform.setFromTransform(transfrom)
        self.__setTurtleToTransform()

    # Suggested by Gemini
    def resizeCanvas(self):         
        imageWidth = self.__canvasMaxX - self.__canvasMinX
        imageHeight = self.__canvasMaxY - self.__canvasMinY

        canvasCentreX = (self.__canvasMaxX + self.__canvasMinX) / 2
        canvasCentreY = (self.__canvasMaxY + self.__canvasMinY) / 2

        halfSpan = max(imageWidth, imageHeight) / 2

        canvasRadius = halfSpan + self.CANVAS_PADDING

        self.__t.screen.setworldcoordinates(
            canvasCentreX - canvasRadius,
            canvasCentreY - canvasRadius,
            canvasCentreX + canvasRadius,
            canvasCentreY + canvasRadius
        )

    def loop(self):
        self.__t.screen.update()
        self.__t.screen.mainloop()