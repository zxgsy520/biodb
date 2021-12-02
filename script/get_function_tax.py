#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse


LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):

    LOG.info("reading message from %r" % file)

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def read_function(file, site=3):

    r = {}

    for line in read_tsv(file, "\t"):
        r[line[0]] = line[site]

    return r


def get_function_tax(file, tax, site=3):

    r = read_function(file, site)

    print("#Gene id\tClassify\tTaxid\tClass")
    for line in read_tsv(tax, "\t"):
        if line[3] not in r:
            continue
        print("%s\t%s\t%s\t%s" % (line[3], r[line[3]], line[1], line[2]))

    return 0


def add_help_args(parser):

    parser.add_argument("input",  metavar='FILE', type=str,
        help="Input cazy annotation result")
    parser.add_argument("-t", "--tax", metavar='FILE', type=str, required=True,
        help="Species annotation result of input gene.")
    parser.add_argument("-s", "--site", metavar='INT', type=int, default=3,
        help="Input the function location and sort it by function, default=3.")

    return parser


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
name:
    get_function_tax.py Obtain the species annotation results and function annotation results of genes
example:
    get_function_tax.py cazy.tsv --tax NR_anno_tax.txt --site 3 > cazy_tax.tsv 
    get_function_tax.py pul.tsv --tax NR_anno_tax.txt --site 4 >pul_tax.tsv

version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args = add_help_args(parser).parse_args()
    get_function_tax(args.input, args.tax, args.site)


if __name__ == "__main__":
    main()
