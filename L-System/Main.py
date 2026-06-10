from imgui_bundle import immapp

from LSystemController import LSystemController
from GUI import GUI

if __name__ == "__main__":
    lSystemController = LSystemController()
    gui = GUI(lSystemController)

    immapp.run(gui_function=gui.draw, window_title="L-Systems", with_implot=True)
