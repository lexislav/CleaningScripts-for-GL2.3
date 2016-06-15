#MenuTitle: Add suffixes to ligatures based on OT features
# encoding: utf-8
# Copyright: Alexnadr Hudeček & Designiq, 2016

SEARCH_THIS_CATEGORIES = ['Letter','Number']
USE_FEATURES = ['liga', 'dlig', 'hlig', 'rlig']

#DO NOT touch following definitions
import re
import os

font = Glyphs.font
renames = {}
totalNumber = 0

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

def appendFeatureSuffix(feature,code,codeL):
	glyphsCount = 0
	featureSet = []
	global renames
	global SEARCH_THIS_CATEGORIES
	glyphsSet = (glyph for glyph in font.glyphs if glyph.category in SEARCH_THIS_CATEGORIES)
	for glyph in glyphsSet:
		splittedGlyphName = os.path.splitext(glyph.name)
		searchedGlyph = " by " + splittedGlyphName[0] + ";"
		searchContentGlyph = "\' by " + splittedGlyphName[0] + ";"
		newGlyphName = splittedGlyphName[0] + "." + feature + splittedGlyphName[1]
		if searchedGlyph in code:
			if searchContentGlyph not in code:
				codeLine = get_code_line(searchedGlyph,codeL)
				first_line_name = get_first_line_name(codeLine,searchedGlyph)
				if first_line_name not in newGlyphName:
					newGlyphName = first_line_name + "." + feature + splittedGlyphName[1]
				featureSet.append( (glyph.name,newGlyphName) )
				glyphsCount += 1
	if len(featureSet) > 0:
		renames.update({feature:featureSet})
	return glyphsCount

def collectRenames():
	global totalNumber
	global USE_FEATURES
	features = (feature for feature in font.features if feature.name in USE_FEATURES)
	for feature in features:
		arrayedCode = get_feature_code(feature.code)
		countGlyphs = 0
		countGlyphs += appendFeatureSuffix(feature.name,feature.code,arrayedCode)
		totalNumber += countGlyphs

def app(font):
    print "*** Starting analyze the font and it's OT features ***\n"
    font.disableUpdateInterface()
    global renames
    collectRenames()
    print "%s glyphs will get suffix by it's OT feature.\n" % totalNumber
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
    font.enableUpdateInterface()
    Glyphs.redraw()
    print "*** Done ****"

app(font)
