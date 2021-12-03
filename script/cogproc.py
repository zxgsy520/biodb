#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "2.0.1"
__author__ = ("Junpeng Fan, Xingguo Zhang",)
__email__ = "jpfan@whu.edu.cn, invicoun@foxmail.com"
__all__ = []


try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


def read_tsv(file, sep=None):

    for line in open(file, encoding='ISO 8859-1'):
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def read_cog_name(file):

    r = {}

    for line in read_tsv(file, "\t"):
        if len(line)>=4:
            name = line[3]
        else:
            name = ""
        r[line[0]] = [line[1], name, line[2]]

    return r


def str2int(string):

    r = []

    for i in string.split(';'):
        r.append(int(i))

    return r


def read_balst_out(file):

    for record in read_tsv(file, "\t"):
        cog = record[1].split('|')[0]
        starts = str2int(record[2])
        ends = str2int(record[3])
        qcov = (sum(ends)-sum(starts)+len(ends))*100.0/int(record[4])
        note = ' '.join(record[5].split()[1::])

        yield [record[0], cog, "Cdd:"+cog, record[2], record[3], record[6], record[7], qcov, note]


def rpsbproc(file, func):

    data = read_cog_name(func)
    print("#qseqid\tsseqid\tdbxref\tclass\tname\tdesc\tqstart\tqend\tevalue\tscore\tcoverage\tnote")

    for record in read_balst_out(file):
        cogan = ""
        for cog in record[1].split(";"):
            if cog in data:
                cogan = data[cog]
             
                break
        if cogan:

            print("\t".join(record[:3] + cogan + record[3:-2] + [format(record[-2], '.2f')] + [record[-1]]))
        else:
            raise Exception("Sequence %s has no COG annotation information" % record[1])
    return 0


def add_hlep_args(parser):

    parser.add_argument('input',
        help='Input the comment result of COG data.')
    parser.add_argument('-n', '--name', metavar='FILE', type=str, required=True,
        help='Input function classification comment file, default=cog-20.def.tab.')

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
    cogproc.py --COG function annotate

attention:
    cogproc.py COG.tsv -f cog-20.def.tab
version: %s
contact:  %s <%s>\
''' % (__version__, " ".join(__author__), __email__))
    args = add_hlep_args(parser).parse_args()

    rpsbproc(args.input, args.name)


if __name__ == "__main__":
    main()
