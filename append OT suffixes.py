#MenuTitle: Append suffix by OT feature
# encoding: utf-8
# Copyright: Alexnadr Hudeček & Designiq, 2016

font = Glyphs.font
renames = {}
totalNumber = 0

def appendFeatureSuffix(feature):
	glyphsCount = 0
	featureSet = []
	global renames
	glyphsSet = (glyph for glyph in font.glyphs if glyph.category in ['Letter','Number'])
	for glyph in glyphsSet:
		searchedGlyph = " by "+glyph.name + ";"
		searchContentGlyph = "\' by "+glyph.name + ";"
		newGlyphName = glyph.name+"."+feature.name
		if searchedGlyph in feature.code:
			if searchContentGlyph not in feature.code:
				#print "%s belongs to feature %s and will be renamed to %s" % (glyph.name,feature.name,newGlyphName)
				glyphsCount += 1
				featureSet.append( (glyph.name,newGlyphName) )
			#else:
			#	print "%s context thing, wont be renamed" % glyph.name
	if len(featureSet) > 0: renames.update({feature.name:featureSet})
	return glyphsCount

def collectRenames():
	global totalNumber
	for feature in font.features:
		countGlyphs = 0
		countGlyphs += appendFeatureSuffix(feature)
		totalNumber += countGlyphs

def app():
    print "*** Starting analyze the font and it's OT features ***\n"
    global renames
    collectRenames()
    print "%s glyphs will renamed by it's OT feature.\n" % totalNumber
    for feature in renames:
		print "Woring with %s feature" % feature
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
