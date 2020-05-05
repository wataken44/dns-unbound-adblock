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


def uniqify(domains):
    dup = []

    for y in range(len(domains)):
        for x in range(len(domains)):
            if y == x:
                continue
            if domains[y].endswith(domains[x]):
                dup.append(domains[y])

    for d in dup:
        domains.remove(d)

    return sorted(list(set(domains)))


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
