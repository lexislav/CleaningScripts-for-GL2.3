# CleaningScripts-for-GL2.3

## Set of scripts for Glyphs 2.3 for Designiq.

Some features requires external config filen in JSON format. You can use font_sidefile_config.json as a master. Make a copy to the same folder as the font You want to process by script and rename json file to the font name. And keep the .json suffix of course.

This way, You can have special config for every font You want to process.

## Features

### [x] Remove original glyph order
Custom parameter "glyphOrder" will be removed.

### [x] Remove all custom parameters
All Custom Parameters will be removed

### Rename Suffixes
__Not finished__

### Add suffixes to ligatures
Reads font_sidefile_config.json (renamed to the font file name). Looks for ligatures defined in file and appends related suffix.

### [x] Remove Unnecessary Glyphs
Reads font_sidefile_config.json (renamed to the font file name).
Search for Unnecessary glyphs defined in file and remove them from font.
