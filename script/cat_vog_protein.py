#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import gzip
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):

    if file.endswith(".gz"):
        fh = gzip.open(file)
    else:
        fh = open(file)

    for line in fh:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        line = line.strip()

        if not line:
            continue

        yield line.split(sep)

    fh.close()


def read_fasta(file):

    '''Read fasta file'''
    if file.endswith(".gz"):
        fp = gzip.open(file)
    elif file.endswith(".fasta") or file.endswith(".fa") or file.endswith(".faa"):
        fp = open(file)
    else:
        raise Exception("%r file format error" % file)

    r = ""
    for line in fp:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()

        if not line:
            continue
        if line.startswith(">"):
            if r:
                yield r.split("\n", 1)
            r = "%s\n" % line.strip(">")
            continue
        r += line.upper()

    if r:
        yield r.split("\n", 1)
    fp.close()


def read_anno(file):

    r = {}

    for line in read_tsv(file, "\t"):
        if line[0].startswith("#"):
            continue
        r[line[0]] = [line[3], line[4]]

    return r


def get_prefix(file):

    file = file.split("/")[-1]

    if "." in file:
        prefix = file.split(".")[0]
    else:
        prefix = file

    return prefix


def cat_vog_protein(files, annotations):

    data = read_anno(annotations)

    for file in files:
        vogid = get_prefix(file)
        if vogid not in data:
            LOG.info("%s exception" % vogid)
            continue
        group, describe = data[vogid]
        for seqid, seq in read_fasta(file):
            seqid, describe = seqid.split(" ", 1)
            print(">{0}|{1}|{2} {3}\n{4}".format(seqid, vogid, group, describe, seq))

    return 0


def add_hlep_args(parser):

    parser.add_argument("input", nargs="+", metavar="FILE", type=str,
        help="Input the original fasta file.")
    parser.add_argument("-a", "--annotations",  metavar="FILE", type=str, default="vog.annotations.tsv.gz",
        help="Input function comment sheet.")

    return parser


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
URL: https://github.com/zxgsy520/biodb
name:
    cat_vog_protein: Handles building the vogdb database

attention:
    cat_vog_protein.py vog_protein/*.faa --annotations vog.annotations.tsv.gz >vogdb.fasta

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    cat_vog_protein(args.input, args.annotations)


if __name__ == "__main__":

    main()
