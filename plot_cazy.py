#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from collections import OrderedDict

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):
    """
    read tsv joined with sep
    :param file: file name
    :param sep: separator
    :return: list
    """
    LOG.info("reading message from %r" % file)

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def read_cazy_classify(file):
    
    family = []
    number = []
    func = []

    for line in read_tsv(file, '\t'):
        family.append(line[0])
        number.append(int(line[1]))
        func.append('%s:%s (%s)' % (line[0], line[2], line[1]))

    return family, number, func


def plot_cazy(family, number, func, prefix):

    # colors = ['#FF4500', '#ADFF2F', '#9ACD32', '#00FFFF', '#0000FF', '#FF00FF']
    colors = ["#0e72cc", "#6ca30f", "#f59311", "#fa4343", "#16afcc", "#85c021",
              "#d12a6a", "#0e72cc", "#6ca30f", "#f59311", "#fa4343", "#16afcc"]
    font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 14,
         }
    font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 14,
         }

    plt.switch_backend('agg')
    fig = plt.figure(figsize=[13.5, 7])

    ax = plt.axes([0.08, 0.08, 0.575, 0.88])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.tick_params(axis='x', length=0, labelsize=14)
    ax.tick_params(axis='y', length=6, width=2, labelsize=14)
    x = range(len(family))
    ax.bar(x, number, width = 0.7, linewidth=1.5, color = colors[0:len(family)], edgecolor='#000000')
    plt.xticks(x, family)
    plt.ylim([0, max(number)+5])
    ax.set_ylabel('Number of sequences', font1)
    
    axt = plt.axes([0.67, 0.08, 0.85, 0.88])
    axt.axis('off')
    axt.spines['top'].set_visible(False)
    axt.spines['right'].set_visible(False)
    axt.spines['bottom'].set_visible(False)
    axt.spines['left'].set_visible(False)
    n = 0.85
    for i in func:
        n = n-0.06
        axt.text(0, n, i, font2)

    plt.savefig('%s.cazy.pdf' % prefix)
    plt.savefig('%s.cazy.png' % prefix, dpi=700)


def add_help(parser):

    parser.add_argument('input', metavar='FILE', type=str,
        help='Input CAZy database annotation classification file, CAZy_classify.tsv')
    parser.add_argument('-p', '--prefix', metavar='STR', type=str, default='out',
        help='The prefix of the output file.')

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
    plot_cazy.py Draw an annotated columnar distribution chart of the CAZy database

attention:
    plot_cazy.py -i CAZy_classify.tsv -p prefix

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_help(parser).parse_args()
    family, number, func = read_cazy_classify(args.input)

    plot_cazy(family, number, func, args.prefix)

if __name__ == "__main__":

    main()
