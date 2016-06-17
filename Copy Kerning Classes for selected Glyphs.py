#MenuTitle: Copy Kerning Classes for selected Glyphs
# encoding: utf-8
# Copyright: Alexnadr Hudeček & Designiq, 2016

import os

KEY_LETTERS = [
"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AE", "OE", "DZ",
"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ae", "oe"
]

ACCENTS = [
"acute", "acutedotaccent", "caron", "carondotaccent", "cedilla", "cedillaacute", "hungarumlaut", "ogonek", "ogonekmacron", "ring", "ringacute",
"ringbelow", "hookabove", "dieresis", "dieresismacron", "dieresisacute", "dieresiscaron", "dieresisgrave", "dieresisbelow", "barreddieresis",
"grave", "dblgrave", "circumflex", "circumflextilde", "circumflexhookabove", "circumflexacute", "circumflexdotbelow", "circumflexgrave",
"circumflexbelow", "dotaccent", "dotaccentmacron", "dotbelow", "dotbelowdotaccent", "dotbelowmacron", "circumflextilde", "macron", "macronacute",
"macrongrave", "slash", "slashacute", "tilde", "tildeacute", "tildedieresis", "tildemacron", "tildebelow", "hook", "stroke", "linebelow",
"palatalhook", "bar", "breve", "breveacute", "brevegrave", "brevedotbelow", "invertedbreve", "brevehookabove", "brevetilde", "dot",
"dotmacron", "dotless", "curl", "commaaccent"
]

#DO NOT edit bellow this line
DefaultKeys = {}
font = Glyphs.font

def renderDefaultKeys():
	global DefaultKeys
	for letter in KEY_LETTERS:
		letterList = []
		for accent in ACCENTS:
			letterList.append(letter + accent)
		DefaultKeys.update({letter:letterList})

def testKernignInfo(glyph,parentGlyph):
    print glyph.name,": LKG-",glyph.leftKerningGroup,", RKG-",glyph.rightKerningGroup,", LMK-",glyph.leftMetricsKey,", RMK-",glyph.rightMetricsKey
    print parentGlyph,": LKG-",font.glyphs[parentGlyph].leftKerningGroup,", RKG-",font.glyphs[parentGlyph].rightKerningGroup,", LMK-",font.glyphs[parentGlyph].leftMetricsKey,", RMK-",font.glyphs[parentGlyph].rightMetricsKey

def copyKerningInfo(glyph,parentGlyph):
    parentLeftKerningGroup = font.glyphs[parentGlyph].leftKerningGroup
    parentRightKerningGroup = font.glyphs[parentGlyph].rightKerningGroup
    if glyph.leftKerningGroup != parentLeftKerningGroup or glyph.rightKerningGroup != parentRightKerningGroup:
        print "%s\'s current kerning L:%s R:%s will be updated from source glyph (%s) to L:%s, R:%s" % (glyph.name,glyph.leftKerningGroup,glyph.rightKerningGroup,parentGlyph,parentLeftKerningGroup,parentRightKerningGroup)
        if parentLeftKerningGroup:
            glyph.leftKerningGroup = parentLeftKerningGroup
        else:
            glyph.leftKerningGroup.leftKerningGroup = ""
        if parentRightKerningGroup:
            glyph.rightKerningGroup = parentRightKerningGroup
        else:
            glyph.rightKerningGroup = ""
        print "%s\'s kerning values after change L:%s R:%s" % (glyph.name,glyph.leftKerningGroup,glyph.rightKerningGroup)
    #else:
        #print "Glyph %s has definition for source glyph %s for copy it\'s kerning, but kerning is already equal." % ( glyph.name, parentGlyph )


def getAllValues():
    DefaultValues = []
    for key in DefaultKeys:
        DefaultValues += DefaultKeys[key]
    return DefaultValues

def getParentGlyph(name):
    for key in DefaultKeys:
        if name in DefaultKeys[key]:
            return key
    else:
        return ""

def copyKerningClasses(glyphs):
    definition = getAllValues()
    for glyph in glyphs:
        noSuffixedGlyphName = os.path.splitext(glyph.name)[0]
        if glyph.name in definition or noSuffixedGlyphName in definition:
            parentGlyph = getParentGlyph(noSuffixedGlyphName)
            if parentGlyph != "":
                if font.glyphs[parentGlyph]:
                    #testKernignInfo(glyph,parentGlyph)
                    copyKerningInfo(glyph,parentGlyph)
                else:
                    print "Oh, no, parent glyph is not in this font."
            else:
                print "Wow, error :-/"
        #else:
            #print "There is no definition for this glyph (%s)" % glyph.name



def app():
    print "*** Start copying Kernign classes on selected glyphs ***\n"

    glyphsInSelection = len(font.selection)
    if glyphsInSelection <= 1:
    	print "\nWARNING: At least two glyphs need to be selected for script to run!\n"
    else:
        renderDefaultKeys()
        copyKerningClasses(font.selection)
	print "*** Done ****"

app()
