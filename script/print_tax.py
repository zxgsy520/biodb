#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse
from collections import OrderedDict

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def split_tax(tax):

    r = OrderedDict()

    for i in tax.split("|"):
        level, value = i.split("__", 1)
        if not value:
            value = "unclassified"
        r[level] = value

    return r


def tax2str(taxdict):

    r = []

    for key, value in taxdict.items():
        r.append('%s__%s' % (key, value))

    return '|'.join(r)


def print_tax(file):

    for line in read_tsv(file, "\t"):
        if len(line) <= 2:
            LOG.info("\t".join(line))
            continue
        if "__|" in line[2]:
            tax = split_tax(line[2])
            line[2] = tax2str(tax)            
        if "Fungi;" not in line[1]:
            print("%s\t%s" % (line[0], line[2]))
            continue
        line[2] = line[2].replace("k__Eukaryota", "k__Fungi", 1)
        print("%s\t%s" % (line[0], line[2]))

    return 0


def add_hlep_args(parser):

    parser.add_argument("input", metavar="FILE", type=str,
        help="Input the preliminary taxonomy file obtained by taxonkit.")

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
    print_tax.py : Get taxonomy file
attention:
    print_tax.py taxonkit.taxonomy >kraken.taxonomy
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    print_tax(args.input)


if __name__ == "__main__":

    main()
