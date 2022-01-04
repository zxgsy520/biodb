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


def process_geneid(file):

    data = OrderedDict()

    for line in read_tsv(file, "\t"):
        geneid = line[0]
        sample, contig, position = geneid.split(".")
        did = "%s.%s" % (sample, contig)
        if did not in data:
            data[did] = []
        data[did].append(int(position))

    return data


def find_gene_family(glist, gap=1, minegene=2, gaps=1):

    r = []
    temp = []
    gs = 0

    for i in sorted(glist):
        if not temp:
            temp.append(i)
            continue
        if i <= (max(temp)+1):
            temp.append(i)
        elif i <= (max(temp)+gap+1):
            gs += 1
            if gs >= (gap+1):
                if len(temp) >=minegene:
                    r.append(temp)
                gs = 0
                temp = [i]
            else:
                temp.append(i)
        else:
            if len(temp) >=minegene:
                r.append(temp)
            gs = 0
            temp = [i]

    return r


def find_pul(file, gap=1, minegene=2, gaps=1):

    data = process_geneid(file)

    print("#Seq_id\tPULs\tStart\tEnd\tGene Number\tAnnotation Genes\tAnnotation rate(%)")
    n = 0
    for seqid in data:
        for temp in find_gene_family(data[seqid], gaps, minegene, gaps):
            start, end = min(temp), max(temp)
            n += 1
            print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(seqid, n, start, end,
                end-start+1, len(temp), len(temp)*100.0/(end-start+1)
                )
            )

    return 0


def add_hlep_args(parser):

    parser.add_argument('input', metavar='FILE', type=str,
        help='Input pul annotation result file(pul.tsv).')
    parser.add_argument('--gap', metavar='INT', type=int, default=1,
        help="Maximum allowable gap size, default=1")
    parser.add_argument("-mg", '--minegene', metavar='INT', type=int, default=2,
        help="Minimum number of genes allowed, default=2")
    parser.add_argument('--gaps', metavar='INT', type=int, default=1,
        help="Minimum number of gaps allowed, default=1")

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
    find_pul.py -- Polysaccharide utilization site prediction

attention:

    find_pul.py pul.tsv >stat_pul.tsv
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    find_pul(args.input, args.gap, args.minegene, args.gaps)


if __name__ == "__main__":
    main()
