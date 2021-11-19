#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import argparse


LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Junpeng Fan, Xingguo Zhang",)
__email__ = "jpfan@whu.edu.cn, invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def read_ko(file):

    r = {}

    for g, k in read_tsv(file, sep="\t"):
        r[g] = k

    return r


def read_pathway(file):

    r = {}

    for g, k in read_tsv(file, sep="\t"):

        if k.startswith("path:map"):
            continue

        if g not in r:
            r[g] = []

        r[g].append(k)

    return r


def deal_with_keg(line):

    line = line.split()
    line = [line[0], line[1], " ".join(line[2::])]

    return line


def read_keg(file):

    r = {}

    for line in open(file, 'r'):
        line = line.strip()

        if not line or line.startswith('#'):
            continue
        if line.startswith('D'):
            line = deal_with_keg(line)
        else:
            continue

        r["ko:%s" % line[1]] = line[2]

    return r


def keggproc(file, ko, pathway, keg):


    ko_dict = read_ko(ko)
    pathway_dict = read_pathway(pathway)
    name_dict = read_keg(keg)

    print("#qseqid\tsseqid\tdbxref\tclass\tname\tdesc\tqstart\tqend\tevalue\tscore\tnote")
    for record in read_tsv(file, sep="\t"):
        if record[1] in ko_dict:
            ko = ko_dict[record[1]]

            if ko in pathway_dict:
                pathway = ";".join(pathway_dict[ko])
            else:
                pathway = "-"
            if ko not in name_dict:
                LOG.info("%s comment information does not exist" % ko)
                LOG.info("Suggest to follow up ko00001.keg")
                continue
            name, _desc = name_dict[ko].split(";")

            if _desc.endswith("]"):
                ec = _desc.split("[")[-1][:-1]
                desc = "[".join(_desc.split("[")[:-1])
            else:
                ec = "-"
                desc = _desc
        else:
            continue

        print("\t".join([record[0], record[1], ko, pathway, name,
                         desc, record[2], record[3], record[4], record[5], ec]))

    return 0


def add_keggproc_help(parser):

    parser.add_argument("input",  metavar='STR', type=str,
        help="Input the kegg comment result file.")
    parser.add_argument("--ko", metavar='STR', type=str, required=True,
        help="Input the mapping table of protein id and ko.")
    parser.add_argument("--keg", metavar='STR', type=str, required=True,
        help="Input the keg comment form, ko00001.keg.")
    parser.add_argument("--pathway", metavar='STR', type=str, required=True,
        help="Input the mapping relationship between ko and pathway.")

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
     keggproc.py: kegg gene function annotation.

attention:
     keggproc.py KEGG.out --ko pep2ko.txt --pathway ko2pathway.tsv --keg ko00001.keg > KEGG.tsv
''')
    args = add_keggproc_help(parser).parse_args()
    keggproc(args.input, args.ko, args.pathway, args.keg)


if __name__ == "__main__":

    main()
