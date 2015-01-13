#!/usr/bin/env python
"""gxargparse_check_path checks for proper ordering of the system path

If gxargparse appears after python stdlib's argparse, it won't behave properly,
thus we provide a small check utility to ensure proper ordering and provide
suggestions if not functional.
"""
import sys, imp, os

def main():
    good_paths = []
    incorrect_ordering = False
    for path in sys.path:
      try:
        (handle, pathname, desc) = imp.find_module('argparse', [path])
        if desc[2] == 5:
            good_paths.append(pathname)
        elif len(good_paths) == 0:
            incorrect_ordering = True
      except:
          pass

    if incorrect_ordering:
        if len(good_paths) == 0:
            print "gxargparse not installed"
        else:
            print "Incorrect ordering, please set\n\n\tPYTHONPATH=%s\n" % (os.path.dirname(good_paths[0]))
    else:
        print "Ready to go!"

if __name__ == '__main__':
    main()
