import numpy as np
from imgui_bundle import imgui, implot

from .MyTurtle import MyTurtle

class ImGuiTurtle(MyTurtle):
    def __init__(self):
        super().__init__()
        self.resetCanvas()

    def draw(self):
        plotFlags = implot.Flags_.equal | implot.Flags_.canvas_only
        if (implot.begin_plot("result", size=imgui.ImVec2(-1, -1), flags=plotFlags)):
            axisFlags = implot.AxisFlags_.auto_fit | implot.AxisFlags_.no_decorations
            implot.setup_axes(x_label="", y_label="", x_flags=axisFlags, y_flags=axisFlags)

            implot.plot_line("", self.x_coords, self.y_coords)
            implot.end_plot()

    def resetCanvas(self):
        if (not isinstance(self._MyTurtle__lines, np.ndarray) or len(self._MyTurtle__lines) == 0):
            self.x_coords = np.array([0])
            self.y_coords = np.array([0])
        else:
            x_segments = self._MyTurtle__lines[:, :, 0]
            y_segments = self._MyTurtle__lines[:, :, 1]
            nans = np.full((len(self._MyTurtle__lines), 1), np.nan)

            self.x_coords = np.hstack((x_segments, nans)).flatten()
            self.y_coords = np.hstack((y_segments, nans)).flatten()
        