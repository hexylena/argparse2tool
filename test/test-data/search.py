#!/usr/bin/env python

import os
import sys

# to invoke own argparse from this directory (test-data) we must put it on the first place in sys.path
argparse_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
sys.path.insert(0, argparse_dir)

import argparse


parser = argparse.ArgumentParser(description="Toy program to search inverted index and "
                                             "print out each line the term appears")

parser.add_argument('mainfile', type=argparse.FileType('r'), help='Text file to be indexed')
parser.add_argument('term', type=str, help='Term for search')

args = parser.parse_args()

mainfile = args.mainfile
indexfile = mainfile.name + ".idx1"
term = args.term

main = mainfile
index = open(indexfile)

st = term + ": "

for a in index:
    if a.startswith(st):
        n = [int(i) for i in a[len(st):].split(", ") if i]
        linenum = 0
        for l in main:
            linenum += 1
            if linenum in n:
                print linenum, l.rstrip()
        break

