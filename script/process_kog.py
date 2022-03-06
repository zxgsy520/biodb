#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def analyze_kog(head):

    head = head.split(None, 2)
    head[0] = head[0].strip("[").strip("]")

    return head


def read_tsv(file):

    LOG.info("Reading message from %r" % file)

    for line in open(file):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("["):
            kog, kogid, desc = line.split(None, 2)
            continue
        if len(line.split(None)) >= 2:
            ath, seqid = line.split(None, 1)
        else:
            seqid = line
        yield (seqid, kog, kogid, desc)
        if "_" in seqid:
            seqid, n = seqid.split("_", 1)
            yield (seqid, kog, kogid, desc)


def read_fasta(file):

    '''Read fasta file'''
    if file.endswith(".gz"):
        fp = gzip.open(file)
    elif file.endswith(".fasta") or file.endswith(".fa"):
        fp = open(file)
    else:
        raise Exception("%r file format error" % file)

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


def process_kog(fasta, file):

    data = {}
    for seqid, kog, kogid, desc in read_tsv(file):
        data[seqid] = [kog, kogid, desc]

    for seqid, seq in read_fasta(fasta):
        kog = ""
        if seqid in data:
            kog, kogid, desc = data[seqid]
        else:
            if "_" in seqid:
                nseqid, n = seqid.split("_", 1)
            if nseqid in data:
                kog, kogid, desc = data[nseqid]
        if kog:
            seqid = "%s|%s %s" % (kogid, seqid, desc)
        print(">%s\n%s" % (seqid, seq))

    return 0


def add_help_args(parser):

    parser.add_argument("input", metavar="FILE", type=str,
        help="Input fasta file")
    parser.add_argument("-k", "--kog", metavar="STR", type=str, required=True,
        help="Input kog file")

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
    process_kog.py: Modify kog format
attention:
    process_kog.py KOG.fasta -k kog >KOG_new.fasta
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))
    args = add_help_args(parser).parse_args()

    process_kog(args.input, args.kog)


if __name__ == "__main__":

    main()
