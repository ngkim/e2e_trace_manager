'''
import os, sys

handler_path=[ "./handlers","./util"] 
for hpath in handler_path:
    if os.path.abspath(hpath) not in sys.path:
        sys.path.append(os.path.abspath(hpath))

print "sys.path= %s" % sys.path
'''