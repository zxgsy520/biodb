#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import gzip
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.3.8"
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


def read_members(file):

    r = {}

    for line in read_tsv(file, "\t"):
        if line[0].startswith("#"):
            continue
        for i in line[4].strip().split(","):
            r[i] = line[0]

    return r


def build_vogdb(file, members, annotations):

    data1 = read_anno(annotations)
    data2 = read_members(members)

    for seqid, seq in read_fasta(file):
        seqid = seqid.split()[0]
        #print(seqid)
        if seqid not in data2:
            LOG.info("Sequence %s exception" % seqid)
            continue
        vogid = data2[seqid]
        if vogid not in data1:
            LOG.info("%s exception" % vogid)
            continue
        group, describe = data1[vogid]
        print(">{0}|{1}|{2} {3}\n{4}".format(seqid, vogid, group, describe, seq))
        #break

    return 0


def add_hlep_args(parser):

    parser.add_argument("input", metavar="STR", type=str,
        help="Input the original fasta file.")
    parser.add_argument("-m", "--members", metavar="FILE", type=str, default="vog.members.tsv.gz",
        help="Input the correspondence table of protein id and classification.")
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
    build_vogdb: Handles building the vogdb database

attention:
    build_vogdb.py vog.proteins.all.fa --members vog.members.tsv.gz --annotations vog.annotations.tsv.gz >vogdb.fasta

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    build_vogdb(args.input, args.members, args.annotations)


if __name__ == "__main__":

    main()
