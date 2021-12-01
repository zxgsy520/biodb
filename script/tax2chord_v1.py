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


def reads_function_tax(file, display=10):

    data = OrderedDict()
    other = 0
    temp = ""
    n = 0

    for line in read_tsv(file, "\t"):
        if line[1] == "Unbacteria":
            continue
        if line[0] not in data:
            if other:
                data[temp]["Other"] = other
            data[line[0]] = OrderedDict()
            other = 0
            temp = line[0]
            n = 0
        if line[1] != "other":
            n += 1
        if n <= display and line[1] != "other":
            data[line[0]][line[1]] = int(line[2])
        else:
            other += int(line[2])
    if other:
        data[temp]["Other"] = other

    return data


def tax2chord(file, display=10):

    data = reads_function_tax(file, display)

    classify = []
    species = []
    for i in data:
        if i not in classify:
            classify.append(i)
        for j in data[i]:
            if j not in species:
                species.append(j)

    print("Classify\t%s" % "\t".join(classify))

    for i in species:
        temp = []
        for j in classify:
            if j not in data:
                temp.append("0")
                continue
            if i not in data[j]:
                temp.append("0")
                continue
            temp.append(str(data[j][i]))
        print("%s\t%s" % (i, "\t".join(temp)))

    return 0


def add_help_args(parser):

    parser.add_argument("input",  metavar='FILE', type=str,
        help="Input gene function and species source annotation statistical results, stat_cazy_tax.tsv")
    parser.add_argument("-d", "--display", metavar='INT', type=int, default=10,
        help="Top X species on display, default=10")

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
    tax2chord.py The result of gene function annotation is transformed into a matrix

example:
    tax2chord.py stat_cazy_tax.tsv >cazy_chord.tsv

stat_cazy_tax.tsv format:
#Function_classification    Species Genes
GT      Eubacteriales   36170
GT      Bacteroidales   10608
GT      unclassified_Bacteria_order     6883
version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args = add_help_args(parser).parse_args()
    tax2chord(args.input, args.display)


if __name__ == "__main__":
    main()
