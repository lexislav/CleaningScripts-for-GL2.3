# CleaningScripts-for-GL2.3

Set of scripts for Glyphs 2.3 for Designiq.

## Config JSONs

Some features requires external config filen in JSON format top specifi ligatures to work with etc.
Scripts checks if there is cleaningscripts_config.json by side of script file. If so, the file is loaded as general config and is used when no font specific json is located. Good to store some general cleaning settings.
You can use cleaningscripts_config.json as a master for both situations - general config file and specific font config file. Make a copy to the same folder as the font You want to process by script and rename json file to the font name. And keep the .json suffix of course.

This way, You can have special config for every font You want to process.

## Features

### Remove original glyph order
Custom parameter "glyphOrder" will be removed.

### Remove all custom parameters
All Custom Parameters will be removed

### Rename Suffixes
__Not finished__

### Add suffixes to ligatures
Reads font_sidefile_config.json (renamed to the font file name). Looks for ligatures defined in file and appends related suffix.

### Remove Unnecessary Glyphs
Reads font_sidefile_config.json (renamed to the font file name).
Search for Unnecessary glyphs defined in file and remove them from font.

## Changelog

### 0.6
Added features:
- renaming suffixes defined in json config file

#### 0.5
Added features:
- checkboxes reorder
- Remove all masters custom parameters
- Remove all OpenType classes, features and feature prefixes from the font
- fixed some minor bugs

#### 0.4
Added general config json file to script. Script loads that config. When no config related to specific font is located, general config is used instead.
