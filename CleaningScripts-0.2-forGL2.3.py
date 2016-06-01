#MenuTitle: Cleaning Scripts 0.1 for G2.3

import vanilla

class AppController:

    def __init__(self):
        pass

    def run(self):
        self.w = self.getWindow()
        self.w.open()

    def getWindow(self):

        out = vanilla.FloatingWindow((310, 205), "SOME Scripts")

        height = 20

        out.textProcess = vanilla.TextBox((15, height, 80, 20), "Process:", sizeStyle = 'regular')
        out.radioInput = vanilla.RadioGroup((80, height, -15, 40), [ "Selected glyphs in current font", "Selected glyphs in all fonts" ], sizeStyle = 'regular')
        out.radioInput.set(AppWorker.INPUT_SELECTED_CURRENT_FONT)

        height += 40 + 20

        out.textApply = vanilla.TextBox((15, height, 80, 20), "Apply:", sizeStyle = 'regular')
        out.checkBoxUpdateGlyphInfo = vanilla.CheckBox((80, height, -15, 19), "Apply Update Glyph Info", value=True, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveGlyphOrder = vanilla.CheckBox((80, height, -15, 19), "Remove original glyph order ", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveAllCustomParameters = vanilla.CheckBox((80, height, -15, 19), "Remove all custom parameters", value=False, sizeStyle = 'regular')
        height += 19

        out.buttonProcess = vanilla.Button((-15 - 80, -15 - 20, -15, -15), "Process", sizeStyle = 'regular', callback=self.process)
        out.setDefaultButton(out.buttonProcess)

        out.spinner = vanilla.ProgressSpinner((15, -15 - 16, 16, 16), sizeStyle = 'regular')

        return out

    # def updateWindow(self, sender):
    #
    #     self.w.textEditSuffix._nsObject.setEditable_(self.w.checkBoxForceSuffix.get())

    def getSettings(self):
        out = {
            "input": self.w.radioInput.get(),
            "options": {
                "UpdateGlyphInfo": self.w.checkBoxUpdateGlyphInfo.get(),
                "RemoveGlyphOrder": self.w.checkBoxRemoveGlyphOrder.get(),
                "RemoveAllCustomParameters": self.w.checkBoxRemoveAllCustomParameters.get(),
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

    def __init__(self):
        pass

    def printLog(self,message):
        self.outputLog += message + '\n'
        print message

    def removeCustomParameter(self, font, key):
        del(font.customParameters[key])

    def processFont(self, font, onlySelected, options):

        message = '# Proccesing font: ' + font.familyName
        glyphs_total = len(font.glyphs)
        self.printLog(message)

        if options["UpdateGlyphInfo"]:
            self.printLog('-- Updating all Glyphs Info (total %s)' % glyphs_total)
            for glyph in font.glyphs:
                print "--- updating %s" % glyph.name
                glyph.updateGlyphInfo

        if options["RemoveGlyphOrder"]:
            if options["RemoveAllCustomParameters"]:
                self.printLog('-- Skipping RemoveGlyphOrder > Remove All custom parametr is do it all')
            elif Glyphs.font.customParameters["glyphOrder"]:
                self.printLog('-- Removing custom glyph order')
                self.removeCustomParameter(font,'glyphOrder')
            else: self.printLog('-- No custom glyph order parameter.')

        if options["RemoveAllCustomParameters"]:
            self.printLog('-- Removing all custom parameters')
            parameters = []
            for customParameter in font.customParameters:
            	parameters.append(customParameter.name)
            if len(parameters) > 0:
                for customParameter in parameters:
                	self.printLog('--- Removing parameter %s' % customParameter)
                	self.removeCustomParameter(font,customParameter)
            else: print "--- No custom parameters found."

        return True

    def start(self, settings):

        self.outputLog = ''
        self.printLog('==== Starting ====')
        if (settings['input'] == self.INPUT_SELECTED_CURRENT_FONT):
            self.printLog("Only current font will be processed")
            self.processFont(Glyphs.font, True, settings['options'])
        elif (settings['input'] == self.INPUT_SELECTED_ALL_FONTS):
            self.printLog("Processing all opened Fonts")
            for font in Glyphs.fonts:
                self.processFont(font, True, settings['options'])
        self.printLog('===== Done. =====')

    def log(self, s):

        self.outputLog += s + '\n'

    def getLog(self):

        return self.outputLog


app = AppController()
app.run()
