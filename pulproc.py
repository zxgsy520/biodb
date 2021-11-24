#!/usr/bin/env python
# -*- coding: utf-8 -*-



import re
import sys
import argparse
import logging

import codecs

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None, encoding=""):
    
    if encoding:
        ft = codecs.open(file, 'r', encoding= 'utf-8', errors='ignore')
    else:
        ft = open(file)

    for line in ft:
        line = line.strip()
        if isinstance(line, bytes):
            line = line.decode('utf-8', errors='ignore')
            #line = line.decode('gbk')

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)
    ft.close()


def read_describe(file):

    r = {}

    for line in read_tsv(file, "\t", "utf-8"):
        r[line[0]] = [line[1], line[6], line[9], line[11], line[2]]

    return r


def pulproc(file, describe):

    r = read_describe(describe)

    ds = 0
    bs = 0
    print("#qseqid\tsseqid\tpulid\tpmid\tDegradation/Biosynthesis\tSubstrate final\tOrganism name\tNotes")
    for line in read_tsv(file, "\t"):
        pulid = line[1].split("_")[0]

        if line[5] in r:
            pulid = line[5]
        elif pulid in r:
            pass
        else:
            continue
        pmid, substrate, organism, types, notes = r[pulid]
        if ("degradation"in types) or ("grada" in types):
            types = "degradation"
            ds += 1
        elif ("biosynthesis"in types) or ("synthes" in types):
            types = "biosynthesis"
            bs += 1
        else:
            LOG.info("Sequence %s type unknown" % line[0])
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(line[0],
            line[1], pulid, pmid, types, substrate, organism, notes)
        )
    LOG.info("Total\tDegradation\tBiosynthesis\n{0:,}\t{1:,}\t{2:,}".format(
              ds+bs, ds, bs)
    )

    return 0


def add_hlep_args(parser):

    parser.add_argument("input", metavar='FILE', type=str,
        help="Input annotation result file(pul.out).")
    parser.add_argument("-d", "--describe", metavar='STR', type=str, required=True,
        help="Input gene description file(PUL.txt).")

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
    pulproc.py: Annotate statistical PUL analysis results

attention:
    pulproc.py  pul.out -d PUL.txt >pul.tsv 2>stat.pul.tsv

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()
    pulproc(args.input, args.describe)


if __name__ == "__main__":

    main()
