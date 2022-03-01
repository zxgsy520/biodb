#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import logging
import argparse

import collections
LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []



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
            seq.append(line)
            continue
        if len(seq) == 2:
            seq[1] += line
        else:
            seq.append(line)

    if len(seq) == 2:
        yield seq
    fp.close()



def split_attr(attributes):

    r = collections.OrderedDict()
    contents = attributes.strip("[").strip("]").split("] [")
   
    for content in contents:
        content = content
        if not content:
            continue
        if "=" not in content:
            print("%r is not a good formated attribute: no tag!")
            continue
        tag, value = content.split("=", 1)
        r[tag] = value

    return r


def read_ncbi_cds(file):

    data = {}

    for seqid, seq in read_fasta(file):
        seqid, attribute = seqid.split(" ", 1)
        attribute = split_attr(attribute)
        if "gene" not in attribute:
            if "locus_tag" in attribute:
                attribute["gene"] = attribute["locus_tag"]
            else:
                attribute["gene"] = attribute["protein"].split()[0]
        if attribute["gene"].isupper():
            pass
        else:
            attribute["gene"] = ""
        #print(attribute["gene"])
        data[attribute["protein_id"]] = (attribute["protein"], attribute["gene"])

    return data


def rename_ncbi_pep(cds, pep):

    data = read_ncbi_cds(cds)

    for seqid, seq in read_fasta(pep):
        seqid, attribute = seqid.split(" ", 1)
        if "[" in attribute:
            species = "OS=%s " % attribute.split("[")[-1].strip("]")
        else:
            seqid = seqid.split("|")[1]
            species = ""
        if seqid not in data:
            LOG.info("sequence %s does not exist" % seqid)
            continue
        protein, gene = data[seqid]
        if not gene or "ORF" in gene:
            #LOG.info(attribute)
            continue
        #print(gene)
        print(">%s %s %sGN=%s\n%s" % (seqid, protein, species, gene, seq))

    return 0



def add_hlep_args(parser):

    parser.add_argument("pep", metavar="FILE", type=str,
        help="Input protein sequence, (fasta).")
    parser.add_argument("-c", "--cds", metavar="FILE", type=str, required=True,
        help="Input CDS sequence, (fasta).")

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
    rename_ncbi_pep.py: Arrange the protein sequences downloaded from ncbi into SwissProt format sequences
attention:
    rename_ncbi_pep.py refseq_pep.fasta --cds refseq_cds.fasta >uniprot_pep.fasta
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    rename_ncbi_pep(args.cds, args.pep)


if __name__ == "__main__":

    main()
