A small python script to load any text based output file (.txt, .DAT, .s1p, .prn, ..) into a .mat file.

Usage:
Add the readout.py to PATH and mymenu.py to PYTHONPATH or simply keep the files in the same directory as the files you wish to load from.

Call the program in cmd:

readout.py {__ARGUMENTS__]

etc:

readout.py .txt (;) ~##,#### 


Options:
-m : Reads under assumtion its a matrix
-ra2b : Read from unique string a to (unique string) b in file --- (NOT WORKING YET)

Filenames are found with .'s in them \t\t\t\t\t\t\t.DAT

Delimiter (if other than one or multiple space(s)) is specifed by ()'s, etc:\t(\t)

To ignore lines with special characters,  use ~x,y\t\t\t\t\tetc:\t~!,#

