#!/usr/bin/env python
"""argparse2tool outputs the path to the dropin replacements for argparse and
click

intended use: `PYTHONPATH=$(argparse2tool) python script.py ...`
"""
import imp
import os
import sys


def main():
    (handle, pathname, desc) = imp.find_module('argparse2tool')
    if desc[2] != 5:
        sys.exit("could not find argparse2tool")
    path = os.path.join(pathname, "dropins")
    if not os.path.exists(path):
        sys.exit("no dropins dir %s" % path)
    if not os.path.exists(os.path.join(path, "argparse")):
        sys.exit("no dropins/argparse dir %s" % path)
    if not os.path.exists(os.path.join(path, "click")):
        sys.exit("no dropins/click dir %s" % path)

    print(path)


if __name__ == '__main__':
    main()
