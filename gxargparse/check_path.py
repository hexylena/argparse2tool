#!/usr/bin/env python
"""gxargparse_check_path checks for proper ordering of the system path

If gxargparse appears after python stdlib's argparse, it won't behave properly,
thus we provide a small check utility to ensure proper ordering and provide
suggestions if not functional.
"""
import sys, imp, os

def main(quiet=False):
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
            if not quiet:
                print "gxargparse not installed"
        else:
            if quiet:
                print "PYTHONPATH=%s " % os.path.dirname(good_paths[0])
            else:
                print "Incorrect ordering, please set\n\n\tPYTHONPATH=%s\n" % (os.path.dirname(good_paths[0]))
    else:
        if not quiet:
            print "Ready to go!"

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        if sys.argv[1] == '-h':
            print """Usage: gxargparse_check_path [-q] [-h]

Check the path for the correct setting to be able to take advantage
of gxargparse. The -q option prints quietly in order to allow for
things like

    user@host:$ $(gxargparse_check_path -q) python script.py
"""
            sys.exit(1)
        elif sys.argv[1] == '-q':
            main(quiet=True)
        else:
            print "Error, unknown flag. Usage: gxargparse_check_path [-q] [-h]"
            sys.exit(2)
