from __future__ import annotations

class Transform:
    def __init__(self, x: float, y: float, angle: float):
        self.__x = x
        self.__y = y
        self.__angle = angle

    def getPosition(self) -> tuple:
        return (self.__x, self.__y)
    
    def getAngle(self) -> float:
        return self.__angle
    
    def setPosition(self, x: float, y: float):
        self.__x = x
        self.__y = y

    def setAngle(self, angle: float):
        self.__angle = angle

    def setFromTransform(self, transform: Transform):
        x, y = transform.getPosition()
        self.setPosition(x, y)
        self.setAngle(transform.getAngle())