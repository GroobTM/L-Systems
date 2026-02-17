class ProductionRule:
    def __init__(self, initialPattern: str, finalPattern: str):
        self.initialPattern = initialPattern
        self.finalPattern = finalPattern

    def matchesInitialPattern(self, pattern: str) -> bool:
        return pattern == self.initialPattern