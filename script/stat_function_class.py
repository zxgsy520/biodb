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

    LOG.info("reading message from %r" % file)

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def read_class(types):

    r = []

    for i in types.split(";"):
        if i in r:
            continue
        r.append(i)

    return r


def split_tax(tax):

    r = OrderedDict()

    for i in tax.split("|"):
        level, value = i.split("__", 1)
        r[level] = value

    return r


def get_level(tax, level):
 
    r = "other"

    if level:
        tax = split_tax(tax)
        if level in tax:
            r = tax[level]
    else:
        r = tax

    return r


def read_function_tax(file, level="", kingdom=""):

    r = {}

    for line in read_tsv(file, "\t"):
        tax = line[3].split(".")[0]
        if kingdom:
            if kingdom not in tax:
                tax = "Un%s" % kingdom.lower()
            else:
                tax = get_level(tax, level)
        else:
            tax = get_level(tax, level)

        for i in read_class(line[1]):
            if i not in r:
                r[i] = {}
            if tax not in r[i]:
                r[i][tax] = 1
            else:
                r[i][tax] += 1
    return r



def stat_function_class(file, level="", kingdom=""):

    r = read_function_tax(file, level, kingdom)

    for i in r:
        for j, values in sorted(r[i].items(), key=lambda d: d[1], reverse=True):
            print("%s\t%s\t%s" % (i, j, values))

    return 0


def add_help_args(parser):

    parser.add_argument("input",  metavar='FILE', type=str,
        help="Input function and species annotation, CAZy_tax.tsv")
    parser.add_argument("-l", "--level", metavar='STR', type=str, default="",
        choices=["k", "p", "c", "o", "f", "g", "s", ""],
        help="Input the displayed species level. choices=[k,p,c,o,f,g,s], default=all.")
    parser.add_argument("-k", "--kingdom", metavar='STR', type=str, default="",
        choices=["Bacteria", "Eukaryota", "Viruses"],
        help="Choose the object of the study. choices=[Bacteria, Eukaryota, Viruses], default=all.")

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
    stat_function_class.py Statistical classification of genes according to function and species

example:
    stat_function_class.py CAZy_tax.tsv -l s >stat_CAZy_species.tsv

CAZy_tax.tsv format:
#Gene id    Cazy    Taxid   Class
gene_id=1_3731192	GT	2	k__Bacteria
version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args = add_help_args(parser).parse_args()
    stat_function_class(args.input, args.level, args.kingdom)


if __name__ == "__main__":
    main()
