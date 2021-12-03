#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse

from collections import OrderedDict

LOG = logging.getLogger(__name__)

__version__ = "1.2.0"
__author__ = ("Xingguo Zhang",)
__email__ = "113178210@qq.com"
__all__ = []


def read_tsv(file, sep=None):

    LOG.info("reading message from %r" % file)

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def read_describe(file):

    r = {}

    for line in read_tsv(file, "\t"):
        if line[0] in r:
            continue

        temp = line[2].lower()
        types = ""

        if "cohesin" in temp:
            types = "Cohesin"
        elif "dockerin" in temp:
            types = "Dockerin"
        elif ("s-layer" in temp) or ("SLH" in line[2]):
            types = "SLH"
        elif "surface" in temp:
            types = "SLH"
        else:
            continue
        desc = "%s (%s) [taxID=%s]" % (line[2], line[4], line[3])

        r[line[0]] = [types, desc]

    return r


def read_fasta(file):

    '''Read fasta file'''
    if file.endswith(".gz"):
        fp = gzip.open(file)
    else:
        fp = open(file)

    seq = []
    for line in fp:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()

        if not line:
            continue
        if line.startswith(">"):
            line = line.strip(">")
            if len(seq) == 2:
                yield seq
            seq = []
            seq.append(line.split()[0])
            continue
        if len(seq) == 2:
            seq[1] += line
        else:
            seq.append(line)

    if len(seq) == 2:
        yield seq
    fp.close()


def deal_with_cazy(file, describe):

    r = read_describe(describe)
    for seqid, seq in read_fasta(file):
        seqid = seqid.split("|")[0]
        if seqid not in r:
            continue
        temp = r[seqid]
        seqid = "%s|%s %s" %  (seqid, temp[0], temp[1])
        print(">%s\n%s" % (seqid, seq))

    return 0


def add_hlep_args(parser):

    parser.add_argument('fasta', metavar='FILE', type=str,
        help='Input protein sequence file, format(fasta, fa.gz')
    parser.add_argument('-d', '--describe', metavar='STR', type=str, required=True,
        help='Input sequence description file')

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
    deal_with_cazy: Process protein sequence and add it to cazy database.
attention:
    deal_with_cazy IPR001119.fasta -d IPR001119.tsv >>cazy.fasta
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    deal_with_cazy(args.fasta, args.describe)


if __name__ == "__main__":

    main()
