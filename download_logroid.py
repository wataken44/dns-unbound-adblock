#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" download_logroid.py


"""

import os
import sys
import urllib.request
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) "}
WHITELIST_OUTPUT = "whitelist/logroid-hosts.txt"
URL = "https://logroid.github.io/adaway-hosts/hosts_allow.txt"


def main():
    os.chdir(BASE_DIR)

    req = urllib.request.Request(URL, headers=HEADERS)
    res = None

    try:
        res = urllib.request.urlopen(req)
    except Exception as e:
        print(e)

    wfp = open(WHITELIST_OUTPUT, "w")

    body = False
    for line in res:
        s = line.decode("utf-8").strip()

        if s == "" or s[0] == "#":
            continue

        wfp.write("%s\n" % s)

    wfp.close()


if __name__ == "__main__":
    main()
