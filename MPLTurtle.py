import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection

from MyTurtle import MyTurtle

class MPLTurtle(MyTurtle):
    def __init__(self):
        super().__init__()

    def draw(self):
        linesToDraw = LineCollection(self._MyTurtle__lines)

        fig, ax = plt.subplots()
        ax.add_collection(linesToDraw)
        ax.autoscale()

        plt.show()