#!/usr/bin/env python

'''
Copies the mod files directory to the target directory. 
Convenient for deploying repo updates the Assetto Corsa mods folder for testing.
'''

from distutils.dir_util import copy_tree

SRC_DIR = "./assettocorsa"
DST_DIR = "H:/Games/Steam/steamapps/common/assettocorsa"

print("\t📁 {}  ->  {}".format(SRC_DIR, DST_DIR))
print("\t⏳ ...")

copy_tree(SRC_DIR, DST_DIR)

print("✅ Deployed!")