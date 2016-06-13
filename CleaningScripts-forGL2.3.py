#MenuTitle: Cleaning Scripts 0.8 for GL2.3
#encoding: utf-8
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

        out = vanilla.FloatingWindow((355, 335), "Cleaning Scripts v0.8")

        height = 20

        out.textProcess = vanilla.TextBox((15, height, 80, 20), "Process:", sizeStyle = 'regular')
        out.radioInput = vanilla.RadioGroup((80, height, -15, 40), [ "All glyphs in current font", "All glyphs in all fonts" ], sizeStyle = 'regular')
        out.radioInput.set(AppWorker.INPUT_SELECTED_CURRENT_FONT)

        height += 40 + 20

        out.textApply = vanilla.TextBox((15, height, 80, 20), "Apply:", sizeStyle = 'regular')
        out.checkBoxRenameIndividualGlyphs = vanilla.CheckBox((80, height, -15, 19), "Rename individual glyphs", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxUpdateGlyphInfo = vanilla.CheckBox((80, height, -15, 19), "Apply Update Glyph Info", value=True, sizeStyle = 'regular')
        height += 19
        out.checkBoxAddSuffixesToLigatures = vanilla.CheckBox((80, height, -15, 19), "Add suffixes to ligatures", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRenameSuffixes = vanilla.CheckBox((80, height, -15, 19), "Rename suffixes", value=False, sizeStyle = 'regular')
        height += 19

        height += 20

        out.textOptions = vanilla.TextBox((15, height, 80, 20), "Remove:", sizeStyle = 'regular')
        out.checkBoxDeleteUnnecessaryGlyphs = vanilla.CheckBox((80, height, -15, 19), "Delete Unnecessary Glyphs", value = False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveGlyphOrder = vanilla.CheckBox((80, height, -15, 19), "original glyph order ", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveAllCustomParameters = vanilla.CheckBox((80, height, -15, 19), "all custom parameters", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveAllMastersCustomParameters = vanilla.CheckBox((80, height, -15, 19), "all masters custom parameters", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveAllFeatures = vanilla.CheckBox((80, height, -15, 19), "all OpenType features, classes, prefixes", value=False, sizeStyle = 'regular')
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
                "RemoveAllMastersCustomParameters": self.w.checkBoxRemoveAllMastersCustomParameters.get(),
                "AddSuffixesToLigatures": self.w.checkBoxAddSuffixesToLigatures.get(),
                "RenameSuffixes": self.w.checkBoxRenameSuffixes.get(),
                "RenameIndividualGlyphs": self.w.checkBoxRenameIndividualGlyphs.get(),
                "RemoveAllFeatures": self.w.checkBoxRemoveAllFeatures.get(),
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

    allGlyphsNames = []

    fontHasConfig = False
    generalConfigExists = False
    generalConfigData = None

    # Setting variables
    configFile = ""
    generalConfigFile = ""
    disablesNiceNames = False



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



    def get_all_font_names(self):
        for glyph in font.glyphs:
            self.allGlyphsNames.append(glyph.name)
        return True



    def get_correct_new_name(self, proposedName):
        self.get_all_font_names
        existingGlyphs = []
        for sGlyph in self.allGlyphsNames:
            if proposedName in sGlyph:
                existingGlyphs.append(sGlyph)
        else:
            if existingGlyphs != []:
                correctedName = proposedName + "." + str(len(existingGlyphs) + 1).zfill(3)
            else:
                 correctedName = proposedName
        return correctedName



    def processFont(self, font, onlySelected, options):

        glyphs_total = len(font.glyphs)
        message = '# Proccesing font: ' + font.familyName + ' (contains %s glyphs)' % glyphs_total
        messlength = len(message)
        self.printLog(message, False)
        message = '-' * messlength
        self.printLog(message, True)

        configFile = os.path.splitext(font.filepath)[0]+'.json'

        Font.disableUpdateInterface()


        if self.file_is_ok(configFile) == True:
                json_file = open(configFile).read()
                if self.is_json(json_file) == True:
                    json_data = self.get_json_data(json_file)
                    self.fontHasConfig = True
                    self.printLog("-- font has json file attached and file seems OK.",True)
                else:
                    self.fontHasConfig = False
                    self.printLog("-- WARNING: font has json file attached but file is not valid json. Some actions may be skipped",True)
        elif self.generalConfigExists:
            self.fontHasConfig = True
            json_data = self.generalConfigData
            self.printLog("-- there is NO json file attached to the font. General script config will be used instead.",True)
        else:
            self.fontHasConfig = False
            json_data = {}
            self.printLog("-- there is NO json file attached to the font or to the script. Some steps may be skipped for that reason.",True)



        if options["RenameIndividualGlyphs"]:
            if self.fontHasConfig == True and 'Rename Individual Glyphs' in json_data:
                self.printLog('-- Renaming individual glyphs in progress.',False)
                countGlyphs = 0
                for line in json_data['Rename Individual Glyphs']:
                    individualGlyphName = line.keys()[0]
                    for sGlyph in line[individualGlyphName]:
                        if font.glyphs[sGlyph]:
                            newName = self.get_correct_new_name(individualGlyphName)
                            print "------ %s found and will be renamed to %s" % (sGlyph, newName)
                            font.glyphs[sGlyph].name = newName
                            countGlyphs += 1
                else:
                    message = "-- %s Individual glyphs have been renamed." % countGlyphs
                    self.printLog(message,True)
            else:
                self.printLog('-- Renaming individual glyphs skipped. Missing, corrupted json file. Or the file has no info for this operation.',False)



        if options["UpdateGlyphInfo"]:
            if font.disablesNiceNames:
                self.printLog('-- WARNING: Custom naming / Nice names is on. Script will turn it off.',False)
                font.disablesNiceNames = False
            self.printLog('-- Updating all Glyphs Info (total %s)' % glyphs_total,False)
            glyphsNames = []
            for glyph in font.glyphs:
                glyphsNames.append(glyph.name)
            for glyphName in glyphsNames:
                print "---updating %s" % glyphName
                font.glyphs[glyphName].updateGlyphInfo()
            else:
                self.printLog('', True)



        if options["AddSuffixesToLigatures"]:
            if self.fontHasConfig == True and 'Suffixes for ligatures' in json_data:
                self.printLog('-- Adding suffixes to ligatures',False)
                countGlyphs = 0
                for ligature in json_data['Suffixes for ligatures']:
                    key = ligature.keys()[0]
                    ligatureGlyphsString = ", ".join(ligature[key])
                    print "--- %s: checking existence of glyphs %s" % (key, ligatureGlyphsString)
                    for lglyphName in ligature[key]:
                        if font.glyphs[lglyphName]:
                            newGlyphName = self.get_correct_new_name(lglyphName + "." + key)
                            print "------ %s found and will be renamed to %s" % (lglyphName, newGlyphName)
                            font.glyphs[lglyphName].name = newGlyphName
                            countGlyphs += 1
                else:
                    message = "-- Defined suffixes added to %s glyphs." % countGlyphs
                    self.printLog(message,True)
            else:
                self.printLog('-- Adding suffixes to ligatures skipped for missing or corrupted json config file',False)



        if options["RenameSuffixes"]:
            if self.fontHasConfig == True and 'Rename suffixes' in json_data:
                self.printLog('-- Renaming suffixes in progress.',False)
                countGlyphs = 0
                keySuffixes = []
                wantedSuffixes = []
                renames = {}

                for line in json_data['Rename suffixes']:
                    currentKey = line.keys()[0]
                    keySuffixes.append(currentKey)
                    wantedSuffixes += line[currentKey]

                for glyph in font.glyphs:
                    currentSuffix = os.path.splitext(glyph.name)
                    cS = currentSuffix[1]
                    if cS != "" and cS in wantedSuffixes:
                        for key in range(len(keySuffixes)):
                            newSuffix = ""
                            if cS in json_data['Rename suffixes'][key][keySuffixes[key]]:
                                newSuffix = keySuffixes[key]
                                break
                        countGlyphs += 1
                        newGlyphName = self.get_correct_new_name(currentSuffix[0] + newSuffix)
                        renames.update({glyph.name: newGlyphName})
                    else:
                        for singleSuffix in wantedSuffixes:
                            if singleSuffix in glyph.name:
                                print "Achtung! Suffix %s without dot in glyph %s. WHat a mess!" % (singleSuffix,glyph.name)
                else:
                    for key in renames:
                        print "---- %s will be renamed to %s" % (key, renames[key])
                        font.glyphs[key].name = renames[key]
                    message = "-- %s glyphs with suffixes were renamed." % countGlyphs
                    self.printLog(message,True)
            else:
                print json_data
                self.printLog('-- Renaming suffixes skipped for missing, corrupted json file. Or the file has no info for this operation.',False)



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
                else: self.printLog('',True)
            else: self.printLog("--- No custom parameters found.",True)



        if options["RemoveAllMastersCustomParameters"]:
            self.printLog('-- Removing all master custom parameters',False)
            parameters = []
            for master in font.masters:
                for customParameter in master.customParameters:
                    parameters.append(customParameter.name)
            if len(parameters) > 0:
                for master in font.masters:
                    for customParameter in parameters:
                        self.printLog('--- Removing master custom parameter %s from master %s' % (customParameter, master),False)
                        del(master.customParameters[customParameter])
                else:
                    self.printLog('',True)
            else: self.printLog("--- No master custom parameters found.",True)



        if options["RemoveAllFeatures"]:
            self.printLog('-- Removing all OpenType features, classes, prefixes',False)

            features = []
            for feature in font.features:
                features.append(feature.name)
            if len(features) > 0:
                for feature in features:
                    self.printLog('--- Removing feature %s' % feature,False)
                    del(font.features[feature])
                else:
                    self.printLog('',True)
            else: self.printLog("--- No OpenType features found.",True)

            classes = []
            for singleClass in font.classes:
                classes.append(singleClass.name)
            if len(classes) > 0:
                for singleClass in classes:
                    self.printLog('--- Removing class %s' % singleClass,False)
                    del(font.classes[singleClass])
                else:
                    self.printLog('',True)
            else: self.printLog("--- No OpenType classes found.",True)

            featurePrefixes = []
            for featurePrefix in font.featurePrefixes:
                featurePrefixes.append(featurePrefix.name)
            if len(featurePrefixes) > 0:
                for featurePrefix in featurePrefixes:
                    self.printLog('--- Removing feature prefix %s' % featurePrefix,False)
                    del(font.featurePrefixes[featurePrefix])
                else:
                    self.printLog('',True)
            else: self.printLog("--- No OpenType feature prefixes found.",True)



        if options["DeleteUnnecessaryGlyphs"]:
            if self.fontHasConfig == True and 'Unnecessary Glyphs' in json_data:
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



        Font.enableUpdateInterface()
        Glyphs.redraw()

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
