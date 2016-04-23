#!/usr/bin/env python

# Toy program to generate inverted index of word to line.
# Takes input text file on stdin and prints output index on stdout.

import sys
import os

# to invoke own argparse from this directory (test-data) we must put it on the first place in sys.path
argparse_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
sys.path.insert(0, argparse_dir)

import argparse


words = {}

parser = argparse.ArgumentParser(description='Generate inverted index of word to line')
parser.add_argument('mainfile', type=argparse.FileType('r'), help='Text file to be indexed')

args = parser.parse_args()

mainfile = args.mainfile
indexfile = mainfile.name + ".idx1"

main = mainfile
index = open(indexfile, "w")

linenum = 0
for l in main:
    linenum += 1
    l = l.rstrip().lower().replace(".", "").replace(",", "").replace(";", "").replace("-", " ")
    for w in l.split(" "):
        if w:
            if w not in words:
                words[w] = set()
            words[w].add(linenum)

for w in sorted(words.keys()):
    index.write("%s: %s" % (w, ", ".join((str(i) for i in words[w]))) + "\n")
