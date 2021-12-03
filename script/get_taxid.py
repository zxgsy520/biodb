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


def get_taxid(file, kingdom):

    site = 9
    if kingdom in ["Fungi", "Metazoa", "Viridiplantae"]:
        site = 8

    for line in read_tsv(file, '|'):
        superkingdom = line[site].strip()
        if not superkingdom:
            continue
        if superkingdom != kingdom:
            continue
        print(line[0].strip())

    return 0


def add_hlep_args(parser):

    parser.add_argument("input", metavar='FILE', type=str,
        help="Input rankedlineage.dmp file.")
    parser.add_argument('-k', '--kingdom', metavar='FILE', type=str,
        choices=["Archaea", "Bacteria", "Eukaryota","Viruses", "Fungi",
        "Metazoa", "Viridiplantae"], default="",
        help="""Input kingdom(Archaea, Bacteria, Eukaryota, Viruses, \
                Fungi, Metazoa, Viridiplantae), default=Bacteria.""")

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
    get_taxid.py  Taxid of the get kingdom

attention:
    get_taxid.py rankedlineage.dmp -k Bacteria >Bacteria.taxid

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    get_taxid(args.input, args.kingdom)


if __name__ == "__main__":

    main()
