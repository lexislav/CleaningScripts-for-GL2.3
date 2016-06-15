#MenuTitle: Add suffixes to ligatures based on OT features
# encoding: utf-8
# Copyright: Alexnadr Hudeček & Designiq, 2016

SEARCH_THIS_CATEGORIES = ['Letter','Number']
USE_FEATURES = ['liga', 'dlig', 'hlig', 'rlig']

#DO NOT touch following definitions
font = Glyphs.font
renames = {}
totalNumber = 0

def appendFeatureSuffix(feature):
	glyphsCount = 0
	featureSet = []
	global renames
	global SEARCH_THIS_CATEGORIES
	glyphsSet = (glyph for glyph in font.glyphs if glyph.category in SEARCH_THIS_CATEGORIES)
	for glyph in glyphsSet:
		searchedGlyph = " by " + glyph.name + ";"
		searchContentGlyph = "\' by " + glyph.name + ";"
		newGlyphName = glyph.name + "." + feature.name
		if searchedGlyph in feature.code:
			if searchContentGlyph not in feature.code:
				glyphsCount += 1
				featureSet.append( (glyph.name,newGlyphName) )
			#else:
			#	print "%s context thing, wont be renamed" % glyph.name
	if len(featureSet) > 0: renames.update({feature.name:featureSet})
	return glyphsCount

def collectRenames():
	global totalNumber
	global USE_FEATURES
	features = (feature for feature in font.features if feature.name in USE_FEATURES)
	for feature in features:
		countGlyphs = 0
		countGlyphs += appendFeatureSuffix(feature)
		totalNumber += countGlyphs

def app():
    print "*** Starting analyze the font and it's OT features ***\n"
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
    print "*** Done ****"

app()
