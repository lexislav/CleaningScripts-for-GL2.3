#MenuTitle: Copy Kerning Classes for selected Glyphs
# encoding: utf-8
# Copyright: Alexnadr Hudeček & Designiq, 2016

import sys
import os
from GlyphsApp import *
import objc
from AppKit import *
from Foundation import *
import traceback

DefaultKeys = {
    "a" : ["aacute", "adieresis", "agrave"],
	"a.sc" : ["adieresis.sc"]
}

font = Glyphs.font

def testKernignInfo(glyph,parentGlyph):
    print glyph.name,": LKG-",glyph.leftKerningGroup,", RKG-",glyph.rightKerningGroup,", LMK-",glyph.leftMetricsKey,", RMK-",glyph.rightMetricsKey
    print parentGlyph,": LKG-",font.glyphs[parentGlyph].leftKerningGroup,", RKG-",font.glyphs[parentGlyph].rightKerningGroup,", LMK-",font.glyphs[parentGlyph].leftMetricsKey,", RMK-",font.glyphs[parentGlyph].rightMetricsKey

def copyKerningInfo(glyph,parentGlyph):
    parentLeftKerningGroup = font.glyphs[parentGlyph].leftKerningGroup
    parentRightKerningGroup = font.glyphs[parentGlyph].rightKerningGroup
    print "%s\'s current kerning L:%s R:%s will be updated from source glyph (%s) to L:%s, R:%s" % (glyph,glyph.leftKerningGroup,glyph.rightKerningGroup,parentGlyph,parentLeftKerningGroup,parentRightKerningGroup)
    print glyph.leftKerningGroup
    print glyph.rightKerningGroup


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
        if glyph.name in definition:
            parentGlyph = getParentGlyph(glyph.name)
            if parentGlyph != "":
                print "Glyph %s has paraent glyph %s for copying kerning" % ( glyph.name, parentGlyph )
                if font.glyphs[parentGlyph]:
                    #testKernignInfo(glyph,parentGlyph)
                    copyKerningInfo(glyph,parentGlyph)
                else:
                    print "Oh, no, parent glyph is not in this font."
            else:
                print "Wow, error :-/"
        else:
            print "There is no definition for this glyph (%s)" % glyph.name



def app():
    print "*** Start copying Kernign classes on selected glyphs ***\n"

    glyphsInSelection = len(font.selection)
    if glyphsInSelection <= 1:
    	print "\nWARNING: At least two glyphs need to be selected for script to run!\n"
    else:
        copyKerningClasses(font.selection)
	print "*** Done ****"

app()
