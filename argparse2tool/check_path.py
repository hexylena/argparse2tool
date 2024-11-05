#!/usr/bin/env python
"""argparse2tool outputs the path to the dropin replacements for argparse and
click

intended use: `PYTHONPATH=$(argparse2tool) python script.py ...`
"""
import importlib.util
import os
import sys


def main():
    spec = importlib.util.find_spec("argparse2tool")
    if spec is None:
        sys.exit("could not find argparse2tool")

    pathname = os.path.dirname(spec.origin)
    path = os.path.join(pathname, "dropins")

    if not os.path.exists(path):
        sys.exit("no dropins dir %s" % path)
    if not os.path.exists(os.path.join(path, "argparse")):
        sys.exit("no dropins/argparse dir %s" % path)
    if not os.path.exists(os.path.join(path, "click")):
        sys.exit("no dropins/click dir %s" % path)

    print(path)


if __name__ == "__main__":
    main()
