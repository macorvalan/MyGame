# Screens in ANSI art used in AU.

`03-2022 MaCorvalan`

All the ANSI screens used in AU (with evennia color tags) and the originals
in ANSI.

Also the python script to convert from ANSI color codes to evennia color tags.

## Using the script

1. Use PHOTOSHOP o GIMP to create a JPG you want.
2. Use ASCII Generator 2 to convert the JPG in ASCII
3. Copy the screen from ASCII Generator 2 (in B&W)
4. Paste the screen in Moebious and color it
5. Save it
6. Export to utf8ans
7. use the script (in terminal) to replace the ansi color to evennia color tags
    Python AU_ANSI_Parser.py -i [inputfile] -o [outputfile]
