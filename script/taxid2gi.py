#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import gzip
import logging
import argparse

from collections import OrderedDict

LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):

    LOG.info("reading message from %r" % file)

    if file.endswith(".gz"):
        fp = gzip.open(file)
    else:
        fp = open(file)

    for line in fp:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        line = line.strip()
        
        if not line or line.startswith("#"):
            continue 
        yield line.split(sep)


def taxid2gi(taxfile, gifile):

    data = set()

    for line in read_tsv(taxfile, '\t'):
        data.add(line[0])

    for line in read_tsv(gifile, '\t'):
        if line[1] in data:
            print(line[0])
    return 0


def add_hlep_args(parser):
    parser.add_argument("tax", metavar="FILE", type=str,
        help="Input taxid file.")
    parser.add_argument("-g", "--gi", metavar="FILE", type=str, default="gi_taxid_nucl.dmp.gz",
        help="Input the file corresponding to gi and taxid, (default=gi_taxid_nucl.dmp.gz).")

    return parser


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
name:
    taxid2gi.py Extract gi based on taxid.

attention:
    taxid2gi.py --tax taxid.txt --gi gi_taxid_nucl.dmp.gz>gi.txt

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    taxid2gi(args.tax, args.gi)


if __name__ == "__main__":

    main()
