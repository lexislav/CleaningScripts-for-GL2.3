#MenuTitle: Compare Two (selected) Glyphs
# -*- coding: utf-8 -*-
__doc__="""
Will compare two selected glyphs.
"""

font = Glyphs.font

def pathsMatch(A,B):

	match = "False"
	looksGood = "False"

	print "matching paths of %s and %s" % (A[0].parent.name,B[0].parent.name)

	for layerIndex in range(len(A)):
  		if len(A[layerIndex].paths) == 0:
  			for component in A[layerIndex].components:
  				if component.componentName == B[layerIndex].parent.name:
  					looksGood = True
  				else:
  					return False
  		elif len(B[layerIndex].paths) == 0:
  			for component in B[layerIndex].components:
  				if component.componentName == A[layerIndex].parent.name:
  					looksGood =  True
  				else:
  					return False
  		else:
  			if A[layerIndex].compareString() == B[layerIndex].compareString():
  				looksGood = "True"
  			#iterate trought paths and nodes here is propably more reliable

	match = looksGood
	return match

def glyphsComparation(A,B):
	match = False
	looksGood = False
	if len(A.layers) == len(B.layers):
		for i in range(len(A.layers)):
			if A.layers[i].name == B.layers[i].name:
				looksGood =  pathsMatch(A.layers,B.layers)
			else:
				looksGood =  False
				break
		else:
			if looksGood == True:
				match = True
	return match

countSelection = len(font.selection)

print "Working with %s \n" % font.familyName
if countSelection <= 1:
	print "At least two glyphs need to be selected for script to run."
else:
	GlyphA = font.selection[0]
	GlyphB = font.selection[1]
	if countSelection > 2:
		print "Too many selected glyphs. Just first two will be compared."
if glyphsComparation(GlyphA,GlyphB) == True:
	print "glyphs match"
else:
	print "glyphs don't match"
