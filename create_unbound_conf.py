#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" create_unbound_conf.py


"""

import glob
import os
import re
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/"


def read_whitelist_regex(filename):
    fp = open(filename)

    r = []

    for line in fp:
        s = re.sub("#.*", "", line.strip())

        if len(s) == 0:
            continue
        r.append(re.compile(s))

    fp.close()

    return r


def read_blacklist_domains(filename, whitelist):
    fp = open(filename)

    d = []

    for line in fp:
        s = re.sub("#.*", "", line.strip())

        if (len(s) == 0) or (s.find(".") == -1):
            continue
        ok = False
        for w in whitelist:
            if w.search(s):
                ok = True
        if ok:
            continue
        d.append(s)

    fp.close()
    return d


def uniqify(src):
    dup = []

    for y in range(len(src)):
        for x in range(len(src)):
            if y == x:
                continue
            if src[y].endswith(src[x]):
                dup.append(src[y])

    dup = sorted(list(set(dup)))
    ret = sorted(list(set(src)))

    for d in dup:
        ret.remove(d)

    return sorted(list(set(ret)))


def main():
    os.chdir(BASE_DIR)

    whitelist = []
    for f in glob.glob("whitelist/*.txt"):
        whitelist += read_whitelist_regex(f)

    blacklist = []
    for f in glob.glob("blacklist/*.txt"):
        blacklist += read_blacklist_domains(f, whitelist)

    fp = open("output/blacklist.conf", "w")
    fp.write("server:\n")
    for domain in uniqify(blacklist):
        fp.write('    local-zone: "%s." static' % domain + "\n")
    fp.close()


if __name__ == "__main__":
    main()
