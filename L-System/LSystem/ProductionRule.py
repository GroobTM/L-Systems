class ProductionRule:
    def __init__(self, rule: str, probability: float = 1):
        self.__rule = rule
        self.__probability = probability

    def getRule(self) -> str:
        return self.__rule
    
    def getProbability(self) -> float:
        return self.__probability
    
    def convertToDict(self) -> dict[str, float]:
        return {
            "rule" : self.__rule,
            "probability": self.__probability
        }
