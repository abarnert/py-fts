#!/usr/bin/python

import os
import sys
import fts

def ftswalk(path):
    f = fts.fts(path, flags=fts.FTS_PHYSICAL | fts.FTS_NOSTAT)
    for ent in f:
    	print(ent.fts_path)

for arg in sys.argv[1:]:
    ftswalk(arg)
