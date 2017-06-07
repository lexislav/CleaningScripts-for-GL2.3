#MenuTitle: Cleaning Scripts 0.9.2 for GL2.3
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

        out = vanilla.FloatingWindow((380, 365), "Cleaning Scripts v0.9.2")

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
        out.checkBoxAddSuffixesToLigaturesOTCode = vanilla.CheckBox((80, height, -15, 19), "Add suffixes to ligatures based on OT code", value=False, sizeStyle = 'regular')
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
        out.checkBoxRemovePUA = vanilla.CheckBox((80, height, -15, 19), "remove PUA", value=False, sizeStyle = 'regular')
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
                "AddSuffixesToLigaturesBasedOnOTCode": self.w.checkBoxAddSuffixesToLigaturesOTCode.get(),
                "RenameSuffixes": self.w.checkBoxRenameSuffixes.get(),
                "RenameIndividualGlyphs": self.w.checkBoxRenameIndividualGlyphs.get(),
                "RemoveAllFeatures": self.w.checkBoxRemoveAllFeatures.get(),
                "RemovePUA": self.w.checkBoxRemovePUA.get(),
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
    json_data = {}
    glyphs_total = 0

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
        self.allGlyphsNames = []
        for glyph in self.font.glyphs:
            self.allGlyphsNames.append(glyph.name)
        return True

    def get_correct_new_name(self, proposedName):
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

    def step_getConfiguration(self):
        if self.file_is_ok(self.configFile) == True:
                json_file = open(self.configFile).read()
                if self.is_json(json_file) == True:
                    self.json_data = self.get_json_data(json_file)
                    self.fontHasConfig = True
                    self.printLog("-- font has json file attached and file seems OK.",True)
                else:
                    self.fontHasConfig = False
                    self.printLog("-- WARNING: font has json file attached but file is not valid json. Some actions may be skipped",True)
        elif self.generalConfigExists:
            self.fontHasConfig = True
            self.json_data = self.generalConfigData
            self.printLog("-- there is NO json file attached to the font. General script config will be used instead.",True)
        else:
            self.fontHasConfig = False
            self.json_data = {}
            self.printLog("-- there is NO json file attached to the font or to the script. Some steps may be skipped for that reason.",True)
        return self.json_data

    def step_removePUA(self):
        if self.options["RemovePUA"]:
            PUAglyphs = []
            self.printLog('-- Removing unicode for glyphs in PUA.',False)
            for glyph in self.font.glyphs:
            	if (glyph.unicode >= "E000" and glyph.unicode <= "F8FF") or (glyph.unicode >= "F0000" and glyph.unicode <= "FFFFD") or (glyph.unicode >= "100000" and glyph.unicode <= "10FFFD"):
            		PUAglyphs.append(glyph.name)
            for glyph in PUAglyphs:
                self.font.glyphs[glyph].unicode = None
            self.printLog("-- Unicode has been removed from %s glyphs originaly in PUA" % len(PUAglyphs),True)

    def step_renameIndividualGlyphs(self):
        if self.options["RenameIndividualGlyphs"]:
            if self.fontHasConfig == True and 'Rename Individual Glyphs' in self.json_data:
                self.printLog('-- Renaming individual glyphs in progress.',False)
                countGlyphs = 0
                renames = {}
                for line in self.json_data['Rename Individual Glyphs']:
                    individualGlyphName = line.keys()[0]
                    for sGlyph in line[individualGlyphName]:
                        if self.font.glyphs[sGlyph]:
                            newName = self.get_correct_new_name(individualGlyphName)
                            renames.update({sGlyph: newName})
                            countGlyphs += 1
                else:
                    for key in renames:
                        print "------ %s found and will be renamed to %s" % (key, renames[key])
                        self.font.glyphs[key].name = renames[key]
                    message = "-- %s Individual glyphs have been renamed." % countGlyphs
                    self.printLog(message,True)
            else:
                self.printLog('-- Renaming individual glyphs skipped. Missing, corrupted json file. Or the file has no info for this operation.',False)

    def step_updateGlyphInfo(self):
        if self.options["UpdateGlyphInfo"]:
            if self.font.disablesNiceNames:
                self.printLog('-- WARNING: Custom naming / Nice names is on. Script will turn it off.',False)
                self.font.disablesNiceNames = False
            self.printLog('-- Updating all Glyphs Info (total %s)' % self.glyphs_total,False)
            self.get_all_font_names()
            errorGlyphs = []
            for glyphName in self.allGlyphsNames:
                print "---updating %s" % glyphName
                if self.font.glyphs[glyphName]:
                    self.font.glyphs[glyphName].updateGlyphInfo(True)
                else:
                    errorGlyphs.append(glyphName)
            else:
                if len(errorGlyphs) > 0:
                    self.printLog('-- WARNING: error updating % s glyphs.' % len(errorGlyphs), False)
                    print '---- ERROR OCCURED IN THESE GLYPHS: %s' % ",".join(errorGlyphs)
                    self.printLog('',True)
                else:
                    self.printLog('', True)
            self.get_all_font_names()

    def step_addSuffixesToLigatures(self):
        if self.options["AddSuffixesToLigatures"]:
            if self.fontHasConfig == True and 'Suffixes for ligatures' in self.json_data:
                self.get_all_font_names()
                self.printLog('-- Adding suffixes to ligatures',False)
                countGlyphs = 0
                for ligature in self.json_data['Suffixes for ligatures']:
                    key = ligature.keys()[0]
                    ligatureGlyphsString = ", ".join(ligature[key])
                    print "--- %s: checking existence of glyphs %s" % (key, ligatureGlyphsString)
                    for lglyphName in ligature[key]:
                        if self.font.glyphs[lglyphName]:
                            newGlyphName = self.get_correct_new_name(lglyphName + "." + key)
                            #print "------ %s found and will be renamed to %s" % (lglyphName, newGlyphName)
                            self.font.glyphs[lglyphName].name = newGlyphName
                            countGlyphs += 1
                else:
                    message = "-- Defined suffixes added to %s glyphs." % countGlyphs
                    self.printLog(message,True)
            else:
                self.printLog('-- Adding suffixes to ligatures skipped for missing or corrupted json config file',False)
        self.get_all_font_names()

    def step_addSuffixesToLigaturesBasedOnOTCode(self):

        def get_feature_code(code):
        	return code.split("\n")

        def get_code_line(searchedGlyph,codeL):
            for line in codeL:
                if searchedGlyph in line:
                    return line
            else:
                return None

        def get_first_line_name(s,f):
            s = s[4:]
            s = s[:-len(f)]
            s = re.sub(r"\s+", '_', s)
            return s

        def collectRenames():
        	totalNumber = 0
        	global USE_FEATURES
        	features = []
        	for feature in font.features:
        		if feature.name in USE_FEATURES:
        			features.append(feature)
        	for feature in features:
        		arrayedCode = get_feature_code(feature.code)
        		countGlyphs = 0
        		countGlyphs += appendFeatureSuffix(feature.name,feature.code,arrayedCode)
        		totalNumber += countGlyphs
            return = totalNumber

        def appendFeatureSuffix(feature,code,codeL):
        	glyphsCount = 0
        	featureSet = []
        	global renames
        	global SEARCH_THIS_CATEGORIES
        	global NOT_SEPARABLE_SUFFIXES
        	glyphsSet = (glyph for glyph in font.glyphs if glyph.category in SEARCH_THIS_CATEGORIES)
        	for glyph in glyphsSet:
        		splittedGlyphName = os.path.splitext(glyph.name)
        		if splittedGlyphName[1] in NOT_SEPARABLE_SUFFIXES:
        			searchedGlyph = " by " + glyph.name + ";"
        			searchContentGlyph = "\' by " + glyph.name + ";"
        		else:
        			searchedGlyph = " by " + splittedGlyphName[0] + ";"
        			searchContentGlyph = "\' by " + splittedGlyphName[0] + ";"
        		newGlyphName = splittedGlyphName[0] + "." + feature + splittedGlyphName[1]
        		if searchedGlyph in code:
        			codeLine = get_code_line(searchedGlyph,codeL)
        			if "\'" not in codeLine:
        				first_line_name = get_first_line_name(codeLine,searchedGlyph)
        				if first_line_name not in newGlyphName:
        					newGlyphName = first_line_name + "." + feature + splittedGlyphName[1]
        				featureSet.append( (glyph.name,newGlyphName) )
        				glyphsCount += 1
        	if len(featureSet) > 0:
        		renames.update({feature:featureSet})
        	return glyphsCount

        self.get_all_font_names()
        self.printLog("",False)
        if self.options["AddSuffixesToLigaturesBasedOnOTCode"]:
            if self.fontHasConfig == True and 'Suffixes to ligatures based on OT features' in self.json_data:
                self.printLog('-- Adding suffixes to ligatures based on OT code',False)
                self.printLog('--- analyzing the font and it's OT features',False)
                global renames
                print "%s glyphs will get suffix by it's OT feature.\n" % collectRenames()
                for feature in renames:
            		print "Working with %s feature" % feature
            		for key,newGlyphName in renames[feature]:
            			print "> %s will be renamed to %s" % (key,newGlyphName)
            			if font.glyphs[key]:
            				font.glyphs[key].name = newGlyphName
            			else:
            				print "! WARNING: This pair has a problem. It was propably renamed with another feature already."
            		else:
            			print "\n"
            else:
                self.printLog('-- Adding suffixes to ligatures skipped for missing or corrupted json config file',False)
        self.get_all_font_names()

    def step_renameSuffixes(self):
        self.get_all_font_names()
        if self.options["RenameSuffixes"]:
            if self.fontHasConfig == True and 'Rename suffixes' in self.json_data:
                self.printLog('-- Renaming suffixes in progress.',False)
                countGlyphs = 0
                keySuffixes = []
                wantedSuffixes = []
                renames = {}

                for line in self.json_data['Rename suffixes']:
                    currentKey = line.keys()[0]
                    keySuffixes.append(currentKey)
                    wantedSuffixes += line[currentKey]

                for glyph in self.allGlyphsNames:
                    currentSuffix = os.path.splitext(glyph)
                    cS = currentSuffix[1]
                    if cS != "" and cS in wantedSuffixes:
                        for key in range(len(keySuffixes)):
                            newSuffix = ""
                            actualSuffixes = self.json_data['Rename suffixes'][key][keySuffixes[key]]
                            if cS in actualSuffixes:
                                newSuffix = keySuffixes[key]
                                break
                        countGlyphs += 1
                        newGlyphName = self.get_correct_new_name(currentSuffix[0] + newSuffix)
                        renames.update({glyph: newGlyphName})
                    for singleSuffix in wantedSuffixes:
                        if (singleSuffix in currentSuffix[0]) and (len(singleSuffix) + currentSuffix[0].find(singleSuffix)) == len(currentSuffix[0]):
                            newSuffix = ""
                            for i in range(len(keySuffixes)):
                                if singleSuffix in self.json_data['Rename suffixes'][i][keySuffixes[i]]:
                                    newSuffix = keySuffixes[i]
                                    break
                            countGlyphs += 1
                            newGlyphName = currentSuffix[0].replace(singleSuffix,newSuffix) + currentSuffix[1]
                            print "---- EXTRA: ",singleSuffix," / ",currentSuffix[0]," in ",glyph," will be replaced with ",newSuffix," to newname: ",newGlyphName
                            renames.update({glyph: newGlyphName})
                else:
                    for key in renames:
                        print "---- %s will be renamed to %s" % (key, renames[key])
                        self.font.glyphs[key].name = renames[key]
                    message = "-- %s suffixes were renamed." % countGlyphs
                    self.printLog(message,True)
            else:
                print self.json_data
                self.printLog('-- Renaming suffixes skipped for missing, corrupted json file. Or the file has no info for this operation.',False)
        self.get_all_font_names()

    def step_removeGlyphOrder(self):
        self.get_all_font_names()
        if self.options["RemoveGlyphOrder"]:
            if self.options["RemoveAllCustomParameters"]:
                self.printLog('-- Skipping RemoveGlyphOrder > Remove All custom parametr is do it all',True)
            elif self.font.customParameters["glyphOrder"]:
                self.printLog('-- Removing custom glyph order',True)
                self.removeCustomParameter(self.font,'glyphOrder')
            else: self.printLog('-- No custom glyph order parameter.',True)

    def step_removeAllCustomParameters(self):
        if self.options["RemoveAllCustomParameters"]:
            self.printLog('-- Removing all custom parameters',False)
            parameters = []
            for customParameter in self.font.customParameters:
            	parameters.append(customParameter.name)
            if len(parameters) > 0:
                for customParameter in parameters:
                	self.printLog('--- Removing parameter %s' % customParameter,False)
                	self.removeCustomParameter(self.font,customParameter)
                else: self.printLog('',True)
            else:
                self.printLog("--- No custom parameters found.",True)

    def step_removeAllMasterCustomParameters(self):
        if self.options["RemoveAllMastersCustomParameters"]:
            self.printLog('-- Removing all master custom parameters',False)
            parameters = []
            for master in self.font.masters:
                for customParameter in master.customParameters:
                    parameters.append(customParameter.name)
            if len(parameters) > 0:
                for master in self.font.masters:
                    for customParameter in parameters:
                        self.printLog('--- Removing master custom parameter %s from master %s' % (customParameter, master),False)
                        del(master.customParameters[customParameter])
                else:
                    self.printLog('',True)
            else: self.printLog("--- No master custom parameters found.",True)

    def step_removeAllOTFeatures(self):
        if self.options["RemoveAllFeatures"]:
            self.printLog('-- Removing all OpenType features, classes, prefixes',False)

            features = []
            for feature in self.font.features:
                features.append(feature.name)
            if len(features) > 0:
                for feature in features:
                    self.printLog('--- Removing feature %s' % feature,False)
                    del(self.font.features[feature])
                else:
                    self.printLog('',True)
            else: self.printLog("--- No OpenType features found.",True)

            classes = []
            for singleClass in self.font.classes:
                classes.append(singleClass.name)
            if len(classes) > 0:
                for singleClass in classes:
                    self.printLog('--- Removing class %s' % singleClass,False)
                    del(self.font.classes[singleClass])
                else:
                    self.printLog('',True)
            else: self.printLog("--- No OpenType classes found.",True)
            featurePrefixes = []
            for featurePrefix in self.font.featurePrefixes:
                featurePrefixes.append(featurePrefix.name)
            if len(featurePrefixes) > 0:
                for featurePrefix in featurePrefixes:
                    self.printLog('--- Removing feature prefix %s' % featurePrefix,False)
                    del(self.font.featurePrefixes[featurePrefix])
                else:
                    self.printLog('',True)
            else: self.printLog("--- No OpenType feature prefixes found.",True)

    def step_removeUnnecessaryGlyphs(self):
        if self.options["DeleteUnnecessaryGlyphs"]:
            if self.fontHasConfig == True and 'Unnecessary Glyphs' in self.json_data:
                self.printLog('-- Removing Unnecessary Glyphs defined in attached file',False)
                countGlyphs = 0
                for uneccessary_glyph in self.json_data['Unnecessary Glyphs']:
                    if self.font.glyphs[uneccessary_glyph]:
                        print "---- removing %s" % uneccessary_glyph
                        del(self.font.glyphs[uneccessary_glyph])
                        countGlyphs += 1
                    else:
                        print "---- Unnecessary glyph not present in font: %s" % uneccessary_glyph
                else: self.printLog("%s glyphs has been removed." % countGlyphs,True)
            else:
                self.printLog('-- Removing Unnecessary Glyphs skipped for missing or corrupted json config file',False)
        self.get_all_font_names()


    def processFont(self, font, onlySelected, options):
        self.options = options
        self.font = font
        self.glyphs_total = len(self.font.glyphs)
        message = '# Proccesing font: ' + self.font.familyName + ' (contains %s glyphs)' % self.glyphs_total
        messlength = len(message)
        self.printLog(message, False)
        message = '-' * messlength
        self.printLog(message, True)

        self.configFile = os.path.splitext(self.font.filepath)[0]+'.json'

        self.font.disableUpdateInterface()

        self.json_data = self.step_getConfiguration()

        self.step_removePUA()
        self.step_renameIndividualGlyphs()
        self.step_updateGlyphInfo()
        self.step_addSuffixesToLigatures()
        self.step_addSuffixesToLigaturesBasedOnOTCode()
        self.step_renameSuffixes()
        self.step_removeGlyphOrder()
        self.step_removeAllCustomParameters()
        self.step_removeAllMasterCustomParameters()
        self.step_removeAllOTFeatures()
        self.step_removeUnnecessaryGlyphs()

        self.font.enableUpdateInterface()
        Glyphs.redraw()

        return True



    def start(self, settings):

        self.generalConfigFile = os.path.split(os.path.realpath("CleaningScripts_forGL2.3.py"))[0]+'/cleaningscripts_config.json'

        self.outputLog = ''
        self.printLog('==== Starting ====',False)

        # Get general config. JSON should be located side by side with sript file.
        if self.file_is_ok(self.generalConfigFile) == True:
            json_file = open(self.generalConfigFile).read()
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
