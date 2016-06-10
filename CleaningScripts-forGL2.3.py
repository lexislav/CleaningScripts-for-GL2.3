#MenuTitle: Cleaning Scripts 0.4 for GL2.3
# encoding: utf-8
"""
CleaningScripts-forGL2.3.py
Created by Alexandr Hudeček on 2016-06-16.
Copyright (c) 2016 odoka.cz. All rights reserved.
"""

import vanilla
import os
import json


class AppController:

    def __init__(self):
        pass

    def run(self):
        self.w = self.getWindow()
        self.w.open()

    def getWindow(self):

        out = vanilla.FloatingWindow((310, 305), "Cleaning Scripts v0.4")

        height = 20

        out.textProcess = vanilla.TextBox((15, height, 80, 20), "Process:", sizeStyle = 'regular')
        out.radioInput = vanilla.RadioGroup((80, height, -15, 40), [ "All glyphs in current font", "All glyphs in all fonts" ], sizeStyle = 'regular')
        out.radioInput.set(AppWorker.INPUT_SELECTED_CURRENT_FONT)

        height += 40 + 20

        out.textApply = vanilla.TextBox((15, height, 80, 20), "Apply:", sizeStyle = 'regular')
        out.checkBoxUpdateGlyphInfo = vanilla.CheckBox((80, height, -15, 19), "Apply Update Glyph Info", value=True, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveGlyphOrder = vanilla.CheckBox((80, height, -15, 19), "Remove original glyph order ", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveAllCustomParameters = vanilla.CheckBox((80, height, -15, 19), "Remove all custom parameters", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxAddSuffixesToLigatures = vanilla.CheckBox((80, height, -15, 19), "Add suffixes to ligatures", value=False, sizeStyle = 'regular')
        height += 19

        height += 20

        out.textOptions = vanilla.TextBox((15, height, 80, 20), "Remove:", sizeStyle = 'regular')
        out.checkBoxDeleteUnnecessaryGlyphs = vanilla.CheckBox((80, height, -15, 19), "Delete Unnecessary Glyphs", value = False, sizeStyle = 'regular')
        height += 19

        out.buttonProcess = vanilla.Button((-15 - 80, -15 - 20, -15, -15), "Process", sizeStyle = 'regular', callback=self.process)
        out.setDefaultButton(out.buttonProcess)

        out.spinner = vanilla.ProgressSpinner((15, -15 - 16, 16, 16), sizeStyle = 'regular')

        return out

    #def updateWindow(self, sender):
    #    self.w.textEditGlyphsNames._nsObject.setEditable_(self.w.checkBoxDeleteGlyphs.get())

    def getSettings(self):
        out = {
            "input": self.w.radioInput.get(),
            "options": {
                "UpdateGlyphInfo": self.w.checkBoxUpdateGlyphInfo.get(),
                "RemoveGlyphOrder": self.w.checkBoxRemoveGlyphOrder.get(),
                "RemoveAllCustomParameters": self.w.checkBoxRemoveAllCustomParameters.get(),
                "AddSuffixesToLigatures": self.w.checkBoxAddSuffixesToLigatures.get(),
                "DeleteUnnecessaryGlyphs": self.w.checkBoxDeleteUnnecessaryGlyphs.get()
            }
        }

        return out

    def process(self, sender):
        self.w.spinner.start()
        worker = AppWorker()
        worker.start(self.getSettings())
        self.w.spinner.stop()
        self.displayLog(worker.getLog())

    def displayLog(self, s):
        log = vanilla.FloatingWindow((360, 480), 'Log')
        log.textEditor = vanilla.TextEditor((0, 0, -1, -1))
        log.textEditor.set(s)
        log.open()


class AppWorker:

    INPUT_SELECTED_CURRENT_FONT = 0
    INPUT_SELECTED_ALL_FONTS    = 1

    outputLog = None

    fontHasConfig = False
    generalConfigExists = False
    generalConfigData = None

    # Setting variables
    configFile = ""
    generalConfigFile = ""

    def __init__(self):
        pass

    def printLog(self, message, addLine):
        self.outputLog += message + '\n'
        if addLine == True:
            self.outputLog += '\n'
            print message + '\n'
        else:
            print message


    def removeCustomParameter(self, font, key):
        del(font.customParameters[key])

    def file_is_ok(self, filePath):
        if os.path.isfile(filePath) and os.access(filePath, os.R_OK):
            return True
        else:
            return False

    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError, e:
            return False
        return True

    def get_json_data(self, myjson):
        return json.loads(myjson)

    def processFont(self, font, onlySelected, options):

        glyphs_total = len(font.glyphs)
        message = '# Proccesing font: ' + font.familyName + ' (contains %s glyphs)' % glyphs_total
        messlength = len(message)
        self.printLog(message, False)
        message = '-' * messlength
        self.printLog(message, True)

        configFile = os.path.splitext(font.filepath)[0]+'.json'

        if self.file_is_ok(configFile) == True:
                json_file = open(configFile).read()
                if self.is_json(json_file) == True:
                    json_data = self.get_json_data(json_file)
                    self.fontHasConfig = True
                    self.fontHasConfig = True
                    self.printLog("-- font has json file attached and file seems OK.",True)
                else:
                    self.fontHasConfig = False
                    self.fontHasConfig = False
                    self.printLog("-- WARNING: font has json file attached but file is not valid json. Some actions may be skipped",True)
        elif self.generalConfigExists:
            self.fontHasConfig = True
            self.fontHasConfig = True
            json_data = self.generalConfigData
            self.printLog("-- there is NO json file attached to the font. General script config will be used instead.",True)
        else:
            self.fontHasConfig = False
            self.fontHasConfig = False
            json_data = None
            self.printLog("-- there is NO json file attached to the font or to the script. Some steps may be skipped for that reason.",True)



        if options["UpdateGlyphInfo"]:
            if font.disablesNiceNames:
                self.printLog('-- WARNING: Can not run Update Glyph Info. Use custom naming is on. You need to turn it off.',True)
            else:
                self.printLog('-- Updating all Glyphs Info (total %s)' % glyphs_total,False)
                glyphsNames = []
                Font.disableUpdateInterface()
                for glyph in font.glyphs:
            	    glyphsNames.append(glyph.name)
                for glyphName in glyphsNames:
                    print "---updating %s" % glyphName
            	    font.glyphs[glyphName].updateGlyphInfo()
                Font.enableUpdateInterface()


        if options["RemoveGlyphOrder"]:
            if options["RemoveAllCustomParameters"]:
                self.printLog('-- Skipping RemoveGlyphOrder > Remove All custom parametr is do it all',True)
            elif Glyphs.font.customParameters["glyphOrder"]:
                self.printLog('-- Removing custom glyph order',False)
                self.removeCustomParameter(font,'glyphOrder',False)
            else: self.printLog('-- No custom glyph order parameter.',False)


        if options["RemoveAllCustomParameters"]:
            self.printLog('-- Removing all custom parameters',False)
            parameters = []
            for customParameter in font.customParameters:
            	parameters.append(customParameter.name)
            if len(parameters) > 0:
                for customParameter in parameters:
                	self.printLog('--- Removing parameter %s' % customParameter,False)
                	self.removeCustomParameter(font,customParameter)
            else: self.printLog("--- No custom parameters found.",True)


        if options["AddSuffixesToLigatures"]:
            if self.fontHasConfig == True and json_data['Suffixes for ligatures']:
                self.printLog('-- Adding suffixes to ligatures',False)
                countGlyphs = 0
                for ligature in json_data['Suffixes for ligatures']:
                    key = ligature.keys()[0]
                    ligatureGlyphsString = ", ".join(ligature[key])
                    print "--- %s: checking existence of glyphs %s" % (key, ligatureGlyphsString)
                    for lglyphName in ligature[key]:
                        if font.glyphs[lglyphName]:
                            newName = lglyphName + "." + key
                            print "------ %s found and will be renamed to %s" % (lglyphName, newName)
                            font.glyphs[lglyphName].name = newName
                            countGlyphs += 1
                else:
                    message = "-- Defined suffixes added to %s glyphs." % countGlyphs
                    self.printLog(message,True)
            else:
                self.printLog('-- Adding suffixes to ligatures skipped for missing or corrupted json config file',False)



        if options["DeleteUnnecessaryGlyphs"]:
            if self.fontHasConfig == True and json_data['Unnecessary Glyphs']:
                self.printLog('-- Removing Unnecessary Glyphs defined in attached file',False)
                countGlyphs = 0
                for uneccessary_glyph in json_data['Unnecessary Glyphs']:
                    if font.glyphs[uneccessary_glyph]:
                        print "---- removing %s" % uneccessary_glyph
                        del(font.glyphs[uneccessary_glyph])
                        countGlyphs += 1
                    else:
                        print "---- Unnecessary glyph not present in font: %s" % uneccessary_glyph
                else: self.printLog("%s glyphs has been removed." % countGlyphs,True)
            else:
                self.printLog('-- Removing Unnecessary Glyphs skipped for missing or corrupted json config file',False)

        #TODO: the other functionalities :-/
        #howtos forother functionalities
        # Add a glyph
        #font.glyphs.append(GSGlyph('adieresis'))
        # Duplicate a glyph under a different name
        #newGlyph = font.glyphs['A'].copy()
        #newGlyph.name = 'A.alt'
        #font.glyphs.append(newGlyph)
        # Delete a glyph


        return True

    def start(self, settings):

        generalConfigFile = os.path.split(os.path.realpath("CleaningScripts_forGL2.3.py"))[0]+'/cleaningscripts_config.json'

        self.outputLog = ''
        self.printLog('==== Starting ====',False)

        # Get general config. JSON should be located side by side with sript file.
        if self.file_is_ok(generalConfigFile) == True:
            json_file = open(generalConfigFile).read()
            if self.is_json(json_file) == True:
                self.generalConfigExists = True
                self.generalConfigData = self.get_json_data(json_file)
                self.printLog("NOTE: General json config found. It will be used when font config is not present.",True)
            else:
                self.generalConfigExists = False
                self.generalConfigData = None
                self.printLog("WARNING: General json config found. But it's not a valid JSON file and cann't be used.",True)
        else:
            self.generalConfigExists = False
            self.generalConfigData = None

        if (settings['input'] == self.fontHasConfig):
            self.printLog("NOTE: Only current font will be processed",True)
            self.processFont(Glyphs.font, True, settings['options'])
        elif (settings['input'] == self.INPUT_SELECTED_ALL_FONTS):
            self.printLog("NOTE: Processing all opened Fonts",True)
            for font in Glyphs.fonts:
                self.processFont(font, True, settings['options'])
        self.printLog('===== Done. =====',False)

    def log(self, s):

        self.outputLog += s + '\n'

    def getLog(self):

        return self.outputLog


app = AppController()
app.run()
