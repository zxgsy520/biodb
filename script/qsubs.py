#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def mkdir(d):
    """
    from FALCON_KIT
    :param d:
    :return:
    """
    d = os.path.abspath(d)
    if not os.path.isdir(d):
        LOG.debug('mkdir {!r}'.format(d))
        os.makedirs(d)
    else:
        LOG.debug('mkdir {!r}, {!r} exist'.format(d, d))

    return d


def check_path(path):

    path = os.path.abspath(path)

    if not os.path.exists(path):
        msg = "File not found '{path}'".format(**locals())
        LOG.error(msg)
        raise Exception(msg)

    return path


def read_shell(file):

    for line in open(file):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        yield line


def split_shell(file):

    r = []

    for line in read_shell(file):
        temp = []
        for i in line.split(";"):
            i = i.strip()
            if not i or i.startswith("#"):
                continue
            i = i.replace("\t", " ")
            temp.append(' '.join(i.split()))
        r.append('\n'.join(temp))

    return r


def check_done(task_id):
    """
    check the status of done task
    :return: success 1 or fail 0
    """
    if os.path.isfile("%s.done" % task_id):
        status = "success"
        LOG.info("task %r run finished" % task_id)
        return 1
    else:
        status = "failed"
        LOG.info("task %r run but failed" % task_id)
        return 0


def write_script(work_dir, script, task_id):
    """
    write script to .sh
    :return:
    """
    script = """\
set -vex
hostname
date
cd {}
echo task start
{}
touch {}.done
echo task done
date
""".format(work_dir, script, task_id)

    mkdir(work_dir)

    script_path = os.path.join(work_dir, "%s.sh" % task_id)
    with open(script_path, "w") as fh:
        fh.write(script)

    return 1


def qsubs(file, work_dir, prefix, thread=1):

    n = 0
    work_dir = mkdir(work_dir)

    for i in split_shell(file):
        n += 1
        task_id = "%s%s" % (prefix, n)
        if check_done("%s/%s" % (work_dir, task_id)):
            continue
        write_script(work_dir, i, task_id)
        script_path = os.path.join(work_dir, "%s.sh" % task_id)
        run_cmd = "qsub -cwd -pe smp {thread} -N {task_id} {script_path}".format(**locals())
        os.popen(run_cmd)
        LOG.info("task %s run" % task_id)

    return 0


def add_hlep_args(parser):

    parser.add_argument('input', metavar='FILE', type=str,
        help='Input shell script commands.')
    parser.add_argument('-w', '--work_dir', metavar='FLIE', type=str, default="work",
        help='Input working path, default=work.')
    parser.add_argument('-t', '--thread', metavar='INT', type=int, default=1,
        help='Input the number of threads required for a single task, default=1.')
    parser.add_argument('-p', '--prefix', metavar='STR', type=str, default="r",
        help='Task prefix number, default=r.')

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
    qsubs  Bulk delivery tasks

attention:
    qsubs txt.sh
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    qsubs(args.input, args.work_dir, args.prefix, args.thread)


if __name__ == "__main__":

    main()
