import imgui_bundle
import glfw
from imgui_bundle import imgui, immapp
from imgui_bundle.imgui import ImVec2

from AlphabetFunction import AlphabetFunction
from MyTurtle.ImGuiTurtle import ImGuiTurtle
from LSystem import LSystem

class GUI:
    def __init__(self):
        self.t = ImGuiTurtle()

        alphabet = {
            "F" : AlphabetFunction(self.t.moveForward, 10),
            "+" : AlphabetFunction(self.t.turnLeft, 30),
            "-" : AlphabetFunction(self.t.turnRight, 30),
            "[" : AlphabetFunction(self.t.pushState),
            "]" : AlphabetFunction(self.t.popState),
            "X" : None
        }

        productionRules = {
            "X": "F[+X][-X]FX",
            "F": "FF"
        }



        lSystem = LSystem(alphabet, "X", productionRules)

        lSystem.createNthGeneration(5)
        lSystem.executeCurrentGeneration(self.t)

    def __draw(self):
        windowWidth, windowHeight = imgui.get_content_region_avail()
        windowWidth -= imgui.get_style().item_spacing.x
        
        imgui.push_style_var(imgui.StyleVar_.window_padding, ImVec2(0, 0))
        if (imgui.begin_child("results", ImVec2(windowWidth * 0.75, windowHeight), child_flags=imgui.ChildFlags_.borders)):
            self.t.draw()
        imgui.end_child()
        imgui.pop_style_var()

        imgui.same_line()

        if (imgui.begin_child("test", ImVec2(windowWidth * 0.25, windowHeight), child_flags=imgui.ChildFlags_.borders)):
            imgui.text("test")
        imgui.end_child()


    def run(self):
        immapp.run(gui_function=self.__draw, window_title="L-Systems", with_implot=True)



gui = GUI()
gui.run()