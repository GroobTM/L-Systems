import imgui_bundle
import glfw
from imgui_bundle import imgui, immapp
from imgui_bundle.imgui import ImVec2

from AlphabetFunction import AlphabetFunction
from MyTurtle.ImGuiTurtle import ImGuiTurtle
from LSystem import LSystem

class GUI:
    def __init__(self):
        self.__t = ImGuiTurtle()

        alphabet = {
            "F" : AlphabetFunction(self.__t.moveForward, 10),
            "+" : AlphabetFunction(self.__t.turnLeft, 30),
            "-" : AlphabetFunction(self.__t.turnRight, 30),
            "[" : AlphabetFunction(self.__t.pushState),
            "]" : AlphabetFunction(self.__t.popState),
            "X" : None
        }

        productionRules = {
            "X": "F[+X][-X]FX",
            "F": "FF"
        }



        self.__lSystem = LSystem(alphabet, "X", productionRules)

        self.__lSystem.createNthGeneration(0)
        self.__lSystem.executeCurrentGeneration(self.__t)

    def __draw(self):
        windowWidth, windowHeight = imgui.get_content_region_avail()
        windowWidth -= imgui.get_style().item_spacing.x
        
        imgui.push_style_var(imgui.StyleVar_.window_padding, ImVec2(0, 0))
        if (imgui.begin_child("results", ImVec2(windowWidth * 0.75, windowHeight), child_flags=imgui.ChildFlags_.borders)):
            self.__t.draw()
        imgui.end_child()
        imgui.pop_style_var()

        imgui.same_line()

        if (imgui.begin_child("controls", ImVec2(windowWidth * 0.25, windowHeight), child_flags=imgui.ChildFlags_.borders)):
            controlWidth, controlHeight = imgui.get_content_region_avail()
            
            imgui.text("Axiom: " + str(self.__lSystem.getCurrentGenerationCount()))
            if (imgui.button("Next Axiom", ImVec2(-1, 0))):
                self.__lSystem.createNextGeneration()
                self.__lSystem.executeCurrentGeneration(self.__t)
                self.__t.resetCanvas()
            if (imgui.button("Reset", ImVec2(-1, 0))):
                self.__lSystem.createNthGeneration(0)
                self.__lSystem.executeCurrentGeneration(self.__t)
                self.__t.resetCanvas()

            if (imgui.collapsing_header("Current Instructions")):
                imgui.text_wrapped(self.__lSystem.getCurrentGeneration())
        imgui.end_child()


    def run(self):
        immapp.run(gui_function=self.__draw, window_title="L-Systems", with_implot=True)



gui = GUI()
gui.run()