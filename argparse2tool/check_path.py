#!/usr/bin/env python
"""argparse2tool_check_path checks for proper ordering of the system path

If argparse2tool appears after python stdlib's argparse, it won't behave properly,
thus we provide a small check utility to ensure proper ordering and provide
suggestions if not functional.
"""
from __future__ import print_function
import sys
import imp
import os
import argparse


def get_args():
    help_text = """Check the path for the correct setting to be able to take advantage of argparse2tool. """
    parser = argparse.ArgumentParser(prog='argparse2tool_check_path', description=help_text)
    parser.add_argument('-q', dest='quiet', action='store_true', help='run quietly')
    return parser.parse_args()


def main():
    args = get_args()

    good_paths = []
    incorrect_ordering = False
    for path in sys.path:
        try:
            (handle, pathname, desc) = imp.find_module('argparse', [path])
            if desc[2] == 5:
                good_paths.append(pathname)
            elif len(good_paths) == 0:
                incorrect_ordering = True
        except Exception:
            pass

    if incorrect_ordering:
        if len(good_paths) == 0:
            if not args.quiet:
                print("argparse2tool not installed")
        else:
            if args.quiet:
                print(os.path.dirname(good_paths[0]))
            else:
                print("Incorrect ordering, please set\n\n\tPYTHONPATH=%s\n" % (os.path.dirname(good_paths[0])))
    else:
        if not args.quiet:
            print("Ready to go!")


if __name__ == '__main__':
    main()
