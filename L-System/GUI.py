import json

from imgui_bundle import imgui
from imgui_bundle.imgui import ImVec2
from imgui_bundle.portable_file_dialogs import open_file, save_file

from LSystem.LSystemController import LSystemController
from LSystem.AlphabetOption import AlphabetOption

# TODO More Alphabet Options

class GUI:
    def __init__(self, lSystemController: LSystemController):
        self.__lSystemController = lSystemController
        self.__lSystemController.resetGeneration()
        self.__lSystemController.executeCurrentGeneration()

        self.__enableControls = True
        self.__settingsChanged = False

        self.__showAlphabetWarning = False
        self.__showGenerationLengthWarning = False
        self.__showHighNWarning = False
        self.__showRemoveLetterWarning = False
        self.__showRuleLetterWarning = False
        self.__showLoadWarning = False
        self.__showSaveLoadError = False

        self.__updateAxiomCounter()

        self.__addAlphabetSelectedOptionIndex = 0
        self.__addAlphabetMinOptionValue = 0
        self.__addAlphabetMaxOptionValue = 0
        self.__addAlphabetLetter = ""
        self.__letterToRemove = ""

        self.__addRuleKey = ""
        self.__addRuleRule = ""
        self.__addRuleProbability = 1.0
        self.__ruleToRemove = ("", "")

        self.__axiom = self.__lSystemController.getAxiom()

        self.__seed = self.__lSystemController.getSeed()

        self.__colour = self.__lSystemController.getColour()

        self.__loadFilePath = None
        self.__saveLoadErrorReason = ""

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
                if (self.__enableControls):
                    axiomFlags = imgui.InputTextFlags_.word_wrap
                    changed, self.__axiom = imgui.input_text_multiline("##axiom", self.__axiom, ImVec2(-1, 0), flags=axiomFlags)
                    if (changed):
                        self.__axiom = self.__axiom.replace("\n", "").replace("\r", "")
                        self.__lSystemController.setAxiom(self.__axiom)
                        self.__settingsChanged = True
                else:
                    imgui.text_wrapped(self.__axiom)

            if (imgui.collapsing_header("Production Rules")):
                self.__createProductionRulesControls(centre)

            if (imgui.collapsing_header("Seed")):
                if (self.__enableControls):
                    imgui.set_next_item_width(-1.0)
                    changed, self.__seed = imgui.input_int("##seed", self.__seed, 0, 0)
                    if (changed):
                        self.__lSystemController.setSeed(self.__seed)
                        self.__settingsChanged = True

                    if (imgui.button("Randomise Seed", ImVec2(-1, 0))):
                        self.__lSystemController.randomiseSeed()
                        self.__seed = self.__lSystemController.getSeed()
                        self.__settingsChanged = True
                        
                else:
                    imgui.text_wrapped(self.__seed)

            if (imgui.collapsing_header("Colour")):
                colourFlags = imgui.ColorEditFlags_.no_inputs
                changed, self.__colour = imgui.color_edit4("Line Colour", self.__colour, flags=colourFlags)
                if (changed):
                    self.__lSystemController.setColour(self.__colour)

            if (imgui.collapsing_header("Save/Load")):
                self.__createSaveLoadControls(centre) 

        imgui.end_child()

    def __updateAxiomCounter(self):
        self.__currentAxiom = self.__lSystemController.getCurrentGenerationCount()
        self.__selectedNthAxiom = self.__currentAxiom

    def __createGenerationControls(self, centre: ImVec2):
        imgui.text("Axiom: " + str(self.__currentAxiom))
        if (not self.__settingsChanged):
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

        if (imgui.button("Initialise" if self.__settingsChanged else "Reset", ImVec2(-1, 0))):
            self.__processReset()
        
        if (imgui.button("Reset to Default", ImVec2(-1, 0))):
            self.__lSystemController.setToDefaults()
            self.__processReset()
        
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
                self.__updateAxiomCounter()
                self.__showGenerationLengthWarning = False

            if (imgui.button("Cancel", ImVec2(-1, 0))):
                imgui.close_current_popup()
                self.__lSystemController.createNthGeneration(self.__currentAxiom)
                self.__showGenerationLengthWarning = False
            imgui.end_popup()

    def __processReset(self):
        if (self.__lSystemController.isAlphabetCompatible()):
            self.__lSystemController.resetLSystem()
            self.__lSystemController.resetGeneration()
            if (self.__lSystemController.lineCountGTEThreshold(100000)):
                self.__showGenerationLengthWarning = True
            else:
                self.__lSystemController.executeCurrentGeneration()
                self.__updateAxiomCounter()
                self.__enableControls = True
                self.__settingsChanged = False
                self.__axiom = self.__lSystemController.getAxiom()
        else:
            self.__showAlphabetWarning = True

    def __processAxiomGeneration(self, createGenerationFunction):
        if (self.__lSystemController.isAlphabetCompatible()):
            createGenerationFunction()
            if (self.__lSystemController.lineCountGTEThreshold(100000)):
                self.__showGenerationLengthWarning = True
            else:
                self.__lSystemController.executeCurrentGeneration()
                self.__updateAxiomCounter()
                self.__enableControls = False
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
            imgui.table_setup_column("##removeLetter", imgui.TableColumnFlags_.width_fixed)
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
                imgui.begin_disabled(not self.__enableControls)
                if (imgui.button("X##" + alphabetKeys[row], ImVec2(30, 0))):
                    self.__showRemoveLetterWarning = True
                    self.__letterToRemove = alphabetKeys[row]
                imgui.end_disabled()
            imgui.end_table()

        imgui.separator()

        imgui.begin_disabled(not self.__enableControls)

        imgui.text("Letter")
        imgui.set_next_item_width(-1.0)
        changed, self.__addAlphabetLetter = imgui.input_text("##letter", self.__addAlphabetLetter)
        if (changed and len(self.__addAlphabetLetter) > 1):
            self.__addAlphabetLetter = self.__addAlphabetLetter[0]

        imgui.text("Option")
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

        allowAdd = len(self.__addAlphabetLetter) == 1 and self.__addAlphabetLetter not in alphabetKeys
        imgui.begin_disabled(not allowAdd)
        if (imgui.button("Add Letter", ImVec2(-1, 0))):
            self.__lSystemController.addToAlphabet(
                self.__addAlphabetLetter,
                selectedOption,
                (self.__addAlphabetMinOptionValue, self.__addAlphabetMaxOptionValue) if hasValues else None
            )
            self.__addAlphabetLetter = ""
            self.__settingsChanged = True
        imgui.end_disabled()
        imgui.end_disabled()

        if (self.__showRemoveLetterWarning):
            def onYes():
                self.__lSystemController.removeFromAlphabet(self.__letterToRemove)
                self.__showRemoveLetterWarning = False
                self.__letterToRemove = ""
                self.__settingsChanged = True
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

    def __createProductionRulesControls(self, centre: ImVec2):
        productionRules = self.__lSystemController.getProductionRules()
        productionRulesKeys = list(productionRules.keys())

        if (imgui.begin_table("Production Rules", 4)):
            imgui.table_setup_column("##key", imgui.TableColumnFlags_.width_fixed)
            imgui.table_setup_column("##rule", imgui.TableColumnFlags_.width_stretch)
            imgui.table_setup_column("##probability", imgui.TableColumnFlags_.width_fixed)
            imgui.table_setup_column("##removeRule", imgui.TableColumnFlags_.width_fixed)
            for row in range(len(productionRules)):
                rules = productionRules[productionRulesKeys[row]]
                for subRow in range(len(rules)):
                    imgui.table_next_row()
                    imgui.table_set_column_index(0)
                    imgui.set_next_item_width(-1.0)
                    imgui.text(productionRulesKeys[row])

                    imgui.table_set_column_index(1)
                    imgui.text_wrapped(rules[subRow].getRule())

                    imgui.table_set_column_index(2)
                    imgui.text(f"({rules[subRow].getProbability():.2f})")

                    imgui.table_set_column_index(3)
                    imgui.begin_disabled(not self.__enableControls)
                    if (imgui.button("X##" + productionRulesKeys[row] + rules[subRow].getRule(), ImVec2(30, 0))):
                        self.__showRuleLetterWarning = True
                        self.__ruleToRemove = (productionRulesKeys[row], rules[subRow].getRule())
                    imgui.end_disabled()
            imgui.end_table()

        imgui.separator()
        imgui.begin_disabled(not self.__enableControls)

        imgui.text("Key")
        imgui.set_next_item_width(-1.0)
        changed, self.__addRuleKey = imgui.input_text("##key", self.__addRuleKey)
        if (changed and len(self.__addRuleKey) > 1):
            self.__addRuleKey = self.__addRuleKey[0]

        imgui.text("Rule")
        ruleFlags = imgui.InputTextFlags_.word_wrap
        changed, self.__addRuleRule = imgui.input_text_multiline("##rule", self.__addRuleRule, ImVec2(-1, 0), flags=ruleFlags)
        if (changed):
            self.__addRuleRule = self.__addRuleRule.replace("\n", "").replace("\r", "")

        imgui.text("Probability")
        imgui.set_next_item_width(-1.0)
        changed, self.__addRuleProbability = imgui.slider_float("##probability", self.__addRuleProbability, 0, 1, format="%.2f")
        if (changed):
            self.__addRuleProbability = round(self.__addRuleProbability, 2)

        allowAdd = len(self.__addRuleKey) == 1 and len(self.__addRuleRule) >= 1 \
            and self.__addRuleRule not in [existingRule.getRule() for existingRule in productionRules.get(self.__addRuleKey, [])] \
            and self.__addRuleProbability > 0
        imgui.begin_disabled(not allowAdd)
        if (imgui.button("Add Letter", ImVec2(-1, 0))):
            self.__lSystemController.addToProductionRules(
                self.__addRuleKey,
                self.__addRuleRule,
                self.__addRuleProbability
            )
            self.__addRuleKey = ""
            self.__addRuleRule = ""
            self.__addRuleProbability = 1
            self.__settingsChanged = True
        imgui.end_disabled()
        imgui.end_disabled()

        if (self.__showRuleLetterWarning):
            def onYes():
                self.__lSystemController.removeFromProductionRules(self.__ruleToRemove[0], self.__ruleToRemove[1])
                self.__showRuleLetterWarning = False
                self.__ruleToRemove = ("", "")
                self.__settingsChanged = True
            def onNo():
                self.__showRuleLetterWarning = False
                self.__ruleToRemove = ("", "")

            self.__createAreYouSureModal(
                "Are you sure?",
                "Are you sure you want to remove this rule?",
                centre,
                yesFunction=onYes,
                noFunction=onNo
                )
            
    def __createSaveLoadControls(self, centre: ImVec2):
        if (imgui.button("Save Settings", ImVec2(-1, 0))):
            window = save_file(
                "Save Settings",
                "L-System Settings.json",
                filters=["JSON Files (*.json)", "*.json"]
            )

            path = window.result()
            if (path):
                try:
                    self.__lSystemController.save(path)
                except (PermissionError):
                    self.__showSaveLoadError = True
                    self.__saveLoadErrorReason = "Permission denied while trying to write file: " + path

        imgui.begin_disabled(not self.__enableControls)
        if (imgui.button("Load Settings", ImVec2(-1, 0))):
            window = open_file(
                "Load Settings",
                filters=["JSON Files (*.json)", "*.json"]
            )

            self.__loadFilePath = window.result()
            if (self.__loadFilePath):
                self.__showLoadWarning = True

                
        imgui.end_disabled()

        if (self.__showLoadWarning):
            def onYes():
                try:
                    self.__lSystemController.load(self.__loadFilePath[0])
                    self.__axiom = self.__lSystemController.getAxiom()
                    self.__colour = self.__lSystemController.getColour()
                except (FileNotFoundError):
                    self.__showSaveLoadError = True
                    self.__saveLoadErrorReason = "File not found: " + self.__loadFilePath[0]
                except (PermissionError):
                    self.__showSaveLoadError = True
                    self.__saveLoadErrorReason = "Permission denied while trying to read file: " + self.__loadFilePath[0]
                except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                    self.__showSaveLoadError = True
                    self.__saveLoadErrorReason = "The file is corrupted: " + self.__loadFilePath[0]

                self.__settingsChanged = True
                self.__showLoadWarning = False
                self.__loadFilePath = None
            
            def onNo():
                self.__showLoadWarning = False
                self.__loadFilePath = None

            self.__createAreYouSureModal(
                "Are you sure?",
                "Loading a file will overwrite your current settings.\nAre you sure you want to continue?",
                centre,
                yesFunction=onYes,
                noFunction=onNo
                )
            
        if (self.__showSaveLoadError):
            self.__createSaveLoadErrorModal(centre)
            
    def __createSaveLoadErrorModal(self, centre: ImVec2):
        load = self.__loadFilePath != None
        title = "Load Error" if load else "Save Error"
        imgui.open_popup(title)
        imgui.set_next_window_pos(centre, imgui.Cond_.appearing, ImVec2(0.5, 0.5))
        if (imgui.begin_popup_modal(title, flags=imgui.WindowFlags_.always_auto_resize)[0]):
            imgui.push_text_wrap_pos(400)
            imgui.text(self.__saveLoadErrorReason)
            imgui.pop_text_wrap_pos()

            if (imgui.button("Okay", ImVec2(-1, 0))):
                imgui.close_current_popup()
                self.__showSaveLoadError = False
            imgui.end_popup()
        
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