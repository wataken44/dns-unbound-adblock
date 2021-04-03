#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" download_adaway.py


"""

import os
import sys
import urllib.request
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) "}
WHITELIST_OUTPUT = "whitelist/logroid-hosts.txt"
BLACKLIST_OUTPUT = "blacklist/logroid-hosts.txt"
URL = "https://logroid.github.io/adaway-hosts/hosts.txt"


def main():
    os.chdir(BASE_DIR)

    req = urllib.request.Request(URL, headers=HEADERS)
    res = None

    try:
        res = urllib.request.urlopen(req)
    except Exception as e:
        print(e)

    wfp = open(WHITELIST_OUTPUT, "w")
    bfp = open(BLACKLIST_OUTPUT, "w")

    wptn = re.compile("^white (.*)")
    bptn = re.compile("^127.0.0.1 (.*)")

    body = False
    for line in res:
        s = line.decode("utf-8").strip()
        if s.find("white list") >= 0:
            body = True

        if not body:
            continue

        wmo = wptn.search(s)
        if wmo:
            wfp.write("%s\n" % wmo.group(1))

        bmo = bptn.search(s)
        if bmo:
            bfp.write("%s\n" % bmo.group(1))

    wfp.close()
    bfp.close()


if __name__ == "__main__":
    main()
