#!/usr/bin/python

from ctypes import *
import os
import sys
import timeit

def oswalk(path):
    for dirpath, dirnames, filenames in os.walk(path, follow_links=False):
        for name in dirnames + filenames:
            print(os.path.join(dirpath, name))

for arg in sys.argv[1:]:
    oswalk(arg)
