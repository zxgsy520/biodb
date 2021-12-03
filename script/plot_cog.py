#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from collections import OrderedDict


LOG = logging.getLogger(__name__)

__version__ = "1.1.1"
__author__ = ("Junpeng Fan, Xingguo Zhang",)
__email__ = "jpfan@whu.edu.cn, invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):
    """
    read tsv joined with sep
    :param file: file name
    :param sep: separator
    :return: list
    """
    LOG.info("reading message from %r" % file)
    if "def.tab" in file:
        fp = open(file, encoding='ISO 8859-1')
    else:
        fp = open(file)

    for line in fp:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)
    fp.close()


def read_cog_function(file):

    r = OrderedDict()

    for line in read_tsv(file, sep="\t"):
        r[line[0]] = line[2]

    return r


def read_cog_name(file):

    r = {}

    for line in read_tsv(file, sep="\t"):
        r[line[0]] = line[1]

    return r


def read_cog_result(file, func2name, cog2func):

    r = {i: set() for i in func2name}

    for record in read_tsv(file, sep="\t"):
        id = record[0]
        for cog in record[1].split(';'):
            if cog in cog2func:
                func = cog2func[cog]
                for i in func:
                    r[i].add(id)

    return r


def plot_cog(cog, func, name, out="out"):

    func2name = read_cog_function(func)
    cog2func = read_cog_name(name)
    cog_dict = read_cog_result(cog, func2name, cog2func)

    label = func2name.keys()
    x = range(len(label))
    y = [len(cog_dict[i]) for i in func2name]

    y_max = max(y) * 1.1

    n = 0

    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    #plt.style.use('seaborn')
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, )

    for f in func2name:
        num = len(cog_dict[f])
        ax.text(num, n, "{0:,}".format(num), fontsize=8, verticalalignment='center', family="Arial", )
        ax.text(y_max / -0.95, n, "[%s] %s" % (f, func2name[f]), fontsize=8, verticalalignment='center',
                horizontalalignment='left', family="Arial",
                )

        n += 1

    ax.barh(x, y, alpha=0.8, tick_label=label)
    ax.set_xlim([y_max / -100, y_max])
    ax.set_ylim([-1, len(x)])
    plt.xticks(fontsize=8, family="Arial", )
    ax.set_yticks([])
    plt.subplots_adjust(top=0.97, left=0.5, right=0.95, bottom=0.07)
    plt.xlabel("Number of Genes", fontsize=10, family="Arial", weight="bold")
    plt.yticks(fontsize=8)

    ax.invert_yaxis()
    plt.savefig("%s.pdf" % out)
    plt.savefig("%s.png" % out, dpi=900)


def set_args():
    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
description:

version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("cog", help="")
    args.add_argument("--func")
    args.add_argument("--name")
    args.add_argument("--out")

    return args.parse_args()


def main():
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    args = set_args()
    plot_cog(args.cog, args.func, args.name, args.out)

if __name__ == "__main__":
    main()
