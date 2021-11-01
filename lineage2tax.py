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

__version__ = "1.0.1"
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
            line = line.decode('utf-8')
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def lineage2tax(file):

    for line in read_tsv(file, '|'):
        print('%s\t%s\t%s' % (line[0].strip(), line[1].strip(), line[2].strip().replace('; ', ';')))

    return 0


def add_hlep_args(parser):
    parser.add_argument("input", help="Input fullnamelineage.dmp file.")

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
    lineage2tax.py  Taxid and species classification level of exported species

attention:
    lineage2tax.py fullnamelineage.dmp >species.taxonomy

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    lineage2tax(args.input)


if __name__ == "__main__":

    main()
