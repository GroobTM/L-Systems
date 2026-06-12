from imgui_bundle import imgui
from imgui_bundle.imgui import ImVec2

from LSystem.LSystemController import LSystemController
from LSystem.AlphabetOption import AlphabetOption

class GUI:
    def __init__(self, lSystemController: LSystemController):
        self.__lSystemController = lSystemController
        self.__lSystemController.resetGeneration()

        self.__showAlphabetWarning = False
        self.__showGenerationLengthWarning = False
        self.__showHighNWarning = False
        self.__showRemoveLetterWarning = False

        self.__updateAxiom()

        self.__addAlphabetSelectedOptionIndex = 0
        self.__addAlphabetMinOptionValue = 0
        self.__addAlphabetMaxOptionValue = 0
        self.__addAlphabetLetter = ""
        self.__letterToRemove = ""

    def draw(self):
        windowWidth, windowHeight = imgui.get_content_region_avail()
        windowWidth -= imgui.get_style().item_spacing.x
        centre = ImVec2(windowWidth * 0.5, windowHeight * 0.5)        
        
        imgui.push_style_var(imgui.StyleVar_.window_padding, ImVec2(0, 0))
        if (imgui.begin_child("results", ImVec2(windowWidth * 0.75, windowHeight), child_flags=imgui.ChildFlags_.borders)):
            self.__lSystemController.drawLSystem()
        imgui.end_child()
        imgui.pop_style_var()

        imgui.same_line()

        if (imgui.begin_child("controls", ImVec2(windowWidth * 0.25, windowHeight), child_flags=imgui.ChildFlags_.borders)):
            self.__createGenerationControls(centre)

            if (imgui.collapsing_header("Current Instructions")):
                imgui.text_wrapped(self.__lSystemController.getCurrentGeneration())

            if (imgui.collapsing_header("Alphabet")):
                self.__createAlphabetControls(centre)

            if (imgui.collapsing_header("Initial Axiom")):
                imgui.text_wrapped(self.__lSystemController.getAxiom())
        imgui.end_child()

    def __updateAxiom(self):
        self.__currentAxiom = self.__lSystemController.getCurrentGenerationCount()
        self.__selectedNthAxiom = self.__currentAxiom

    def __createGenerationControls(self, centre: ImVec2):
        imgui.text("Axiom: " + str(self.__currentAxiom))
        if (imgui.button("Next Axiom", ImVec2(-1, 0))):
            self.__processNextAxiomGeneration()
        if (imgui.button("Nth Axiom", ImVec2(-1, 0))):
            imgui.open_popup("Select Axiom")

        imgui.set_next_window_pos(centre, imgui.Cond_.appearing, ImVec2(0.5, 0.5))
        if (imgui.begin_popup_modal("Select Axiom", flags=imgui.WindowFlags_.always_auto_resize)[0]):
            changed, self.__selectedNthAxiom = imgui.slider_int("Select Nth Axiom", self.__selectedNthAxiom, v_min=0, v_max=20)
            if (imgui.button("Okay", ImVec2(-1, 0))):
                imgui.close_current_popup()
                self.__processNthAxiomGeneration()
            imgui.end_popup()

        if (imgui.button("Reset", ImVec2(-1, 0))):
            self.__lSystemController.resetGeneration()
            self.__updateAxiom()
        
        # ----- Incompatible Alphabet Modal -----
        if (self.__showAlphabetWarning):
            imgui.open_popup("Incompatible Alphabet")

        imgui.set_next_window_pos(centre, imgui.Cond_.appearing, ImVec2(0.5, 0.5))
        if (imgui.begin_popup_modal("Incompatible Alphabet", flags=imgui.WindowFlags_.always_auto_resize)[0]):
            imgui.push_text_wrap_pos(400)
            imgui.text("Initial axiom or production rules contain characters that are not present in the current alphabet.")
            imgui.pop_text_wrap_pos()
            if (imgui.button("Okay", ImVec2(-1, 0))):
                imgui.close_current_popup()
                self.__showAlphabetWarning = False
            imgui.end_popup()

        # ----- High Nth Generation Modal -----
        if (self.__showHighNWarning):
            def onYes():
                self.__processAxiomGeneration(lambda: self.__lSystemController.createNthGeneration(self.__selectedNthAxiom))
                self.__showHighNWarning = False
            
            def onNo():
                self.__showHighNWarning = False

            self.__createAreYouSureModal(
                "High Nth Generation",
                "Depending the complexity of the production rules, it may take a while to generated this axiom.\nDo you want to continue?",
                centre,
                yesFunction=onYes,
                noFunction=onNo
                )

        # ----- Large Generation Modal -----
        if (self.__showGenerationLengthWarning):
            imgui.open_popup("Large Generation")

        imgui.set_next_window_pos(centre, imgui.Cond_.appearing, ImVec2(0.5, 0.5))
        if (imgui.begin_popup_modal("Large Generation", flags=imgui.WindowFlags_.always_auto_resize)[0]):
            imgui.push_text_wrap_pos(400)
            if (self.__lSystemController.lineCountGTEThreshold(1000000)):
                imgui.text("WARNING: Generated axiom is over 1,000,000 lines long. This is very likey to cause serious performance issues.")
            elif (self.__lSystemController.lineCountGTEThreshold(500000)):
                imgui.text("WARNING: Generated axiom is over 500,000 lines long. This is likey to cause performance issues.")
            else:
                imgui.text("WARNING: Generated axiom is over 100,000 lines long. You may start to experience performance issues.")
            imgui.pop_text_wrap_pos()

            if (imgui.button("Continue", ImVec2(-1, 0))):
                imgui.close_current_popup()
                self.__lSystemController.executeCurrentGeneration()
                self.__updateAxiom()
                self.__showGenerationLengthWarning = False

            if (imgui.button("Cancel", ImVec2(-1, 0))):
                imgui.close_current_popup()
                self.__lSystemController.createNthGeneration(self.__currentAxiom)
                self.__showGenerationLengthWarning = False
            imgui.end_popup()

    def __processAxiomGeneration(self, createGenerationFunction):
        if (self.__lSystemController.isAlphabetCompatible()):
            createGenerationFunction()
            if (self.__lSystemController.lineCountGTEThreshold(100000)):
                self.__showGenerationLengthWarning = True
            else:
                self.__lSystemController.executeCurrentGeneration()
                self.__updateAxiom()
        else:
            self.__showAlphabetWarning = True

    def __processNextAxiomGeneration(self):
        self.__processAxiomGeneration(lambda: self.__lSystemController.createNextGeneration())

    def __processNthAxiomGeneration(self):
        if (self.__currentAxiom != self.__selectedNthAxiom):
            if (self.__selectedNthAxiom >= 10):
                self.__showHighNWarning = True
            else:
                self.__processAxiomGeneration(lambda: self.__lSystemController.createNthGeneration(self.__selectedNthAxiom))

    def __createAlphabetControls(self, centre: ImVec2):
        alphabet = self.__lSystemController.getAlphabet()
        alphabetKeys = list(alphabet.keys())
        alphabetOptions = self.__lSystemController.getAlphabetOptions()
        alphabetOptionsKeys = list(alphabetOptions.keys())
        alphabetOptionsNames = [key.value for key in alphabetOptionsKeys]

        if (imgui.begin_table("Alphabet", 3)):
            imgui.table_setup_column("##letter", imgui.TableColumnFlags_.width_fixed)
            imgui.table_setup_column("##function", imgui.TableColumnFlags_.width_stretch)
            imgui.table_setup_column("##close", imgui.TableColumnFlags_.width_fixed)
            for row in range(len(alphabet)):
                imgui.table_next_row()
                imgui.table_set_column_index(0)
                imgui.set_next_item_width(-1.0)
                imgui.text(alphabetKeys[row])

                imgui.table_set_column_index(1)
                alphabetFunc = alphabet[alphabetKeys[row]]
                alphabetFuncValue = alphabetFunc.getValue()

                imgui.set_next_item_width(-1.0)
                if (alphabetFuncValue == None):
                    imgui.text_wrapped(alphabet[alphabetKeys[row]].getAlphabetOption().value)
                else:
                    if (alphabetFuncValue[0] == alphabetFuncValue[1]):
                        imgui.text_wrapped(f"{alphabet[alphabetKeys[row]].getAlphabetOption().value} ({alphabetFuncValue[0]})")
                    else:
                        imgui.text_wrapped(f"{alphabet[alphabetKeys[row]].getAlphabetOption().value} ({alphabetFuncValue[0]} - {alphabetFuncValue[1]})")
                
                imgui.table_set_column_index(2)
                if (imgui.button("X##" + alphabetKeys[row], ImVec2(30, 0))):
                    self.__showRemoveLetterWarning = True
                    self.__letterToRemove = alphabetKeys[row]

            imgui.end_table()
            imgui.separator()

            imgui.set_next_item_width(-1.0)
            changed, self.__addAlphabetSelectedOptionIndex = imgui.combo("##option", self.__addAlphabetSelectedOptionIndex, alphabetOptionsNames)
            selectedOption = alphabetOptionsKeys[self.__addAlphabetSelectedOptionIndex]
            hasValues = selectedOption != AlphabetOption.PUSH and selectedOption != AlphabetOption.POP and selectedOption != AlphabetOption.STOP
            if (hasValues):
                if (selectedOption == AlphabetOption.LEFT or selectedOption == AlphabetOption.RIGHT):
                    self.__addAlphabetMaxOptionValue = max(0, min(180, self.__addAlphabetMaxOptionValue))
                    self.__addAlphabetMinOptionValue = max(0, min(180, self.__addAlphabetMinOptionValue))

                    imgui.text_wrapped("Max Angle")
                    imgui.set_next_item_width(-1.0)
                    changed, self.__addAlphabetMaxOptionValue = imgui.slider_int("##maxAngle", self.__addAlphabetMaxOptionValue, 0, 180)
                    if (changed and self.__addAlphabetMaxOptionValue < self.__addAlphabetMinOptionValue):
                        self.__addAlphabetMinOptionValue = self.__addAlphabetMaxOptionValue

                    imgui.text_wrapped("Min Angle")
                    imgui.set_next_item_width(-1.0)
                    changed, self.__addAlphabetMinOptionValue = imgui.slider_int("##minAngle", self.__addAlphabetMinOptionValue, 0, 180)
                    if (changed and self.__addAlphabetMaxOptionValue < self.__addAlphabetMinOptionValue):
                        self.__addAlphabetMaxOptionValue = self.__addAlphabetMinOptionValue
                else:
                    imgui.text_wrapped("Max Value")
                    imgui.set_next_item_width(-1.0)
                    changed, self.__addAlphabetMaxOptionValue = imgui.input_int("##maxValue", self.__addAlphabetMaxOptionValue, 0, 180)
                    if (changed and self.__addAlphabetMaxOptionValue < self.__addAlphabetMinOptionValue):
                        self.__addAlphabetMinOptionValue = self.__addAlphabetMaxOptionValue

                    imgui.text_wrapped("Min Value")
                    imgui.set_next_item_width(-1.0)
                    changed, self.__addAlphabetMinOptionValue = imgui.input_int("##minValue", self.__addAlphabetMinOptionValue, 0, 180)
                    if (changed and self.__addAlphabetMaxOptionValue < self.__addAlphabetMinOptionValue):
                        self.__addAlphabetMaxOptionValue = self.__addAlphabetMinOptionValue

            imgui.text("Letter")
            imgui.set_next_item_width(-1.0)
            changed, self.__addAlphabetLetter = imgui.input_text("#letter", self.__addAlphabetLetter)
            if (changed and len(self.__addAlphabetLetter) > 1):
                self.__addAlphabetLetter = self.__addAlphabetLetter[0]

            allowAdd = len(self.__addAlphabetLetter) == 1 and self.__addAlphabetLetter not in alphabetKeys
            imgui.begin_disabled(not allowAdd)
            if (imgui.button("Add Letter", ImVec2(-1, 0))):
                self.__lSystemController.addToAlphabet(
                    self.__addAlphabetLetter,
                    selectedOption,
                    (self.__addAlphabetMinOptionValue, self.__addAlphabetMaxOptionValue) if hasValues else None
                )
                self.__addAlphabetLetter = ""
            imgui.end_disabled()

        if (self.__showRemoveLetterWarning):
            def onYes():
                self.__lSystemController.removeFromAlphabet(self.__letterToRemove)
                self.__showRemoveLetterWarning = False
                self.__letterToRemove = ""
            def onNo():
                self.__showRemoveLetterWarning = False
                self.__letterToRemove = ""

            self.__createAreYouSureModal(
                "Are you sure?",
                "Are you sure you want to remove this letter?",
                centre,
                yesFunction=onYes,
                noFunction=onNo
                )









    def __createAreYouSureModal(self, title:str, text: str, centre: ImVec2, yesFunction = None, noFunction = None):
        imgui.open_popup(title)
        imgui.set_next_window_pos(centre, imgui.Cond_.appearing, ImVec2(0.5, 0.5))
        if (imgui.begin_popup_modal(title, flags=imgui.WindowFlags_.always_auto_resize)[0]):
            imgui.push_text_wrap_pos(400)
            imgui.text(text)
            imgui.pop_text_wrap_pos()

            if (imgui.button("Yes", ImVec2(-1, 0))):
                imgui.close_current_popup()
                if (yesFunction != None):
                    imgui.close_current_popup()
                    yesFunction()

            if (imgui.button("Cancel", ImVec2(-1, 0))):
                imgui.close_current_popup()
                if (noFunction != None):
                    imgui.close_current_popup()
                    noFunction()
                    
            imgui.end_popup()