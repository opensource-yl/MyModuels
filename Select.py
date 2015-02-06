import sys
import os
Script = os.path.basename(sys.argv[0])
if len(sys.argv) < 2:
    print "Usage:\n" \
          "    ./%s File Proporty" %Script
    exit(1)

File = sys.argv[1]
if os.path.isfile(File):
    pass
else:
    print "Not a regular file. Please check."
    exit(2)

ProPorty = float(sys.argv[2])
if 0 <= ProPorty <= 9:
    pass
else:
    print "Not a regular proporty. Please check."
    exit(3)

def GetFile(file, proporty):
    f=open(file)
    for line in f:
        try:
            Pro=line.split()[3]
        except IndexError:
            return
        if Pro and (Pro != 'None_property_yet'):
            Pro = float(Pro)
            if Pro >= ProPorty:
                print line
            else:
                continue
        else:
            continue

GetFile(File, ProPorty)
