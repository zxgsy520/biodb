#!/usr/bin/env python
# -*- coding: utf-8 -*-

CAZY_CLASS = {
    "GH": "Glycoside Hydrolases",
    "GT": "Glycosyl Transferases",
    "PL": "Polysaccharide Lyases",
    "CE": "Carbohydrate Esterases",
    "AA": "Auxiliary Activities",
    "CBM": "Carbohydrate-Binding Modules",
    "SLH": "S-layer homology domain",
    "Cohesin": "Cohesin domain",
    "Dockerin": "Dockerin domain"}


import re
import sys
import argparse
import logging

LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def read_activ(file):

    activ_dict = {}

    for line in read_tsv(file, '\t'):
        if len(line)<=1:
            line.append("")
        activ_dict[line[0]] = line[1].strip()

    return activ_dict


def read_subfam(file):

    subfam_dit = {}

    for line in read_tsv(file, '\t'):
        subfam_dit[line[1]] = [line[2], line[0]]

    return subfam_dit


def cut_type(tlist):

    r = []
    pr = ""

    for i in tlist:
        for j in i.split("_"):
            try:
                pr = re.search("(\D+)", j).group(1)
                r.append(j)
            except:
                r.append("%s%s" % (pr, j))

    return r



def output_cazy(cazy, activ, subfam, output):

    activ_dict = read_activ(activ)
    if subfam:
        subfam_dit = read_subfam(subfam)
    else:
        subfam_dit = {}
    cazy_dict = {}

    print("#qseqid\tsseqid\tnote\tclass\tdesc")
    for line in read_tsv(cazy, '\t'):
        refseq = line[1].strip()
        temp = refseq.split('|')
        seqid = temp[0]

        notes = []
        classs = []
        descs = []
        for typeid in cut_type(temp[1::]):
            if typeid in activ_dict:
                if typeid in notes:
                    continue
                notes.append(typeid)
                descs.append(activ_dict[typeid])
                classs.append(re.search("(\D+)", typeid).group(1))
            else:
                if typeid not in CAZY_CLASS:
                    continue
                notes.append(typeid)
                descs.append(line[-1])
                classs.append(typeid)
                

        if seqid in subfam_dit:
            typeid = subfam_dit[seqid][1]
            if typeid in notes:
                pass
            else:
                if typeid in activ_dict:
                    notes.append(typeid)
                    classs.append(re.search("(\D+)", typeid).group(1))
                    descs.append(activ_dict[typeid])
            
        print("{}\t{}\t{}\t{}\t{}".format(line[0], refseq, ";".join(notes), ";".join(classs), ";".join(descs)))

        for clasid in classs:
            if clasid not in cazy_dict:
                cazy_dict[clasid] = [line[0]]
                continue
            cazy_dict[clasid].append(line[0])

    output = open(output, "w")

    output.write("#class\tnumber\tdesc\tgene\n")
    for line in sorted(cazy_dict.items(),key = lambda x:len(x[1])):
        output.write("{}\t{}\t{}\t{}\n".format(line[0], len(line[1]), CAZY_CLASS[line[0]], ";".join(line[1])))
    output.close()


def add_help(parser):

    parser.add_argument('input', metavar='FILE', type=str,
        help='Input the matching annotation file of CAZy, CAZy.out')
    parser.add_argument('--activ', metavar='FILE', type=str,  required=True,
        help='Input CAZy types of documentation, CAZy.activities.txt.')
    parser.add_argument('--subfam', metavar='FILE', type=str,  default="",
        help='Input the corresponding file of each id and classification of CAZy, CAZy.subfam.ec.txt')
    parser.add_argument('-o', '--output', metavar='STR', type=str, default='cazy_classify.tsv',
        help='The name of the output file.')

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
    cazyproc.py Organize and comment on CAZy database comparison results

attention:
    cazyproc.py CAZy.out --activ CAZy.activities.txt --subfam CAZy.subfam.ec.txt -o cazy_classify.tsv >cazy.tsv

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_help(parser).parse_args()

    output_cazy(args.input, args.activ, args.subfam, args.output)


if __name__ == "__main__":

    main()
