#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" create_unbound_conf.py


"""

import collections
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
        d.append(s.lower())

    fp.close()
    return d


def uniqify(src, whitelist):

    tree = Tree()

    for d in src:
        tree.add_domain(d)

    # do wfs
    queue = collections.deque()
    for k, v in tree.get_root().get_children().items():
        queue.append(v)

    domains = []
    while len(queue) > 0:
        leaf = queue.popleft()

        if None in leaf.get_children():
            domains.append(leaf.get_domain())
        else:
            for k, v in leaf.get_children().items():
                queue.append(v)

    ret = []

    for d in domains:
        ok = False
        for w in whitelist:
            if w.search(d):
                ok = True
        if ok:
            continue
        ret.append(d)

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
    for domain in uniqify(blacklist, whitelist):
        fp.write('    local-zone: "%s." static' % domain + "\n")
    fp.close()


def test():
    tree = Tree()
    tree.add_domain("www.youtube.com")
    tree.add_domain("youtube.com")
    tree.add_domain("google.com")
    tree.add_domain("ipv6.google.com")
    tree.add_domain("www.yahoo.co.jp")
    tree.add_domain("www.goo.ne.jp")
    tree.dump()

    return


class Tree:
    def __init__(self):
        self._root = Leaf("", "")

    def add_domain(self, domain):
        arr = reversed(domain.split("."))

        d = ""
        ptr = self._root
        for s in arr:
            if d != "":
                d = "." + d
            d = s + d
            ptr.add_child(d, s)
            ptr = ptr.get_child(s)

        ptr.add_child(d, None)

    def get_root(self):
        return self._root

    def dump(self):
        self._root.dump()


class Leaf:
    def __init__(self, domain, subdomain):
        self._domain = domain
        self._subdomain = subdomain
        self._children = {}

    def add_child(self, domain, subdomain):
        if subdomain not in self._children:
            self._children[subdomain] = Leaf(domain, subdomain)

    def get_child(self, subdomain):
        if subdomain in self._children:
            return self._children[subdomain]

        return None

    def get_children(self):
        return self._children

    def get_domain(self):
        return self._domain

    def dump(self, depth=0):
        print("  " * depth + str(self._subdomain) + " => " + str(self._domain))

        for k, v in self._children.items():
            v.dump(depth + 1)


if __name__ == "__main__":
    main()
