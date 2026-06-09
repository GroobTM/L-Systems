import numpy as np
from imgui_bundle import imgui, implot

from .MyTurtle import MyTurtle

class ImGuiTurtle(MyTurtle):
    def __init__(self):
        super().__init__()

        self.x_coords = None
        self.y_coords = None


    def __convertLines(self):
            x_segments = self._MyTurtle__lines[:, :, 0]
            y_segments = self._MyTurtle__lines[:, :, 1]
            nans = np.full((len(self._MyTurtle__lines), 1), np.nan)

            self.x_coords = np.hstack((x_segments, nans)).flatten()
            self.y_coords = np.hstack((y_segments, nans)).flatten()

    def draw(self):
        if (not (isinstance(self.x_coords, np.ndarray) and isinstance(self.y_coords, np.ndarray))):
            self.__convertLines()

        plotFlags = implot.Flags_.equal | implot.Flags_.canvas_only
        if (implot.begin_plot("result", size=imgui.ImVec2(-1, -1), flags=plotFlags)):
            axisFlags = implot.AxisFlags_.auto_fit | implot.AxisFlags_.no_decorations
            implot.setup_axes(x_label="", y_label="", x_flags=axisFlags, y_flags=axisFlags)

            implot.plot_line("", self.x_coords, self.y_coords)
            implot.end_plot()