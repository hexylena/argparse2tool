#!/usr/bin/env python

"""List the locations of accessible sequence regions in a FASTA file.

Inaccessible regions, e.g. telomeres and centromeres, are masked out with N in
the reference genome sequence; this script scans those to identify the
coordinates of the accessible regions (those between the long spans of N's).

DEPRECATED -- use "cnvkit.py access" instead.
"""

import argparse
import sys

import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


AP = argparse.ArgumentParser(description=__doc__)
AP.add_argument("fa_fname",
                help="Genome FASTA file name")
AP.add_argument("-s", "--min-gap-size", type=int, default=5000,
                help="""Minimum gap size between accessible sequence
                regions.  Regions separated by less than this distance will
                be joined together. [Default: %(default)s]""")
AP.add_argument("-x", "--exclude", action="append", default=[],
                help="""Additional regions to exclude, in BED format. Can be
                used multiple times.""")
AP.add_argument("-o", "--output",
                type=argparse.FileType('w'), default=sys.stdout,
                help="Output file name")
args = AP.parse_args()


# Closes over args.output
def write_row(chrom, run_start, run_end):
    args.output.write("%s\t%s\t%s\n" % (chrom, run_start, run_end))
    args.output.flush()
