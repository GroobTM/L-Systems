from imgui_bundle import imgui
from imgui_bundle.imgui import ImVec2

from LSystemController import LSystemController

class GUI:
    def __init__(self, lSystemController: LSystemController):
        self.__lSystemController = lSystemController
        self.__lSystemController.resetGeneration()

    def draw(self):
        windowWidth, windowHeight = imgui.get_content_region_avail()
        windowWidth -= imgui.get_style().item_spacing.x
        
        imgui.push_style_var(imgui.StyleVar_.window_padding, ImVec2(0, 0))
        if (imgui.begin_child("results", ImVec2(windowWidth * 0.75, windowHeight), child_flags=imgui.ChildFlags_.borders)):
            self.__lSystemController.drawLSystem()
        imgui.end_child()
        imgui.pop_style_var()

        imgui.same_line()

        if (imgui.begin_child("controls", ImVec2(windowWidth * 0.25, windowHeight), child_flags=imgui.ChildFlags_.borders)):
            imgui.text("Axiom: " + str(self.__lSystemController.getCurrentGenerationCount()))
            if (imgui.button("Next Axiom", ImVec2(-1, 0))):
                self.__lSystemController.generateNextGeneration()
            if (imgui.button("Reset", ImVec2(-1, 0))):
                self.__lSystemController.resetGeneration()

            if (imgui.collapsing_header("Current Instructions")):
                imgui.text_wrapped(self.__lSystemController.getCurrentGeneration())

            if (imgui.collapsing_header("Alphabet")):
                imgui.text("test")
        imgui.end_child()