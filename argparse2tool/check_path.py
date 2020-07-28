#!/usr/bin/env python
"""argparse2tool_check_path checks for proper ordering of the system path

If argparse2tool appears after python stdlib's argparse, it won't behave properly,
thus we provide a small check utility to ensure proper ordering and provide
suggestions if not functional.
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
