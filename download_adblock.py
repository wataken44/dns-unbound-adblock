#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" download_adblock.py


"""

import datetime
import os
import re
import sys
import urllib.request

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) "}
OUTPUT = "blacklist/adblock.txt"
URL = "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt"


def main():
    os.chdir(BASE_DIR)

    now = datetime.datetime.now()

    req = urllib.request.Request(URL, headers=HEADERS)
    res = None

    try:
        res = urllib.request.urlopen(req)
    except Exception as e:
        print(e)
        return

    ptn = re.compile("^\|\|(.*)\^")

    fp = open(OUTPUT, "w")

    for line in res:
        s = line.decode("utf_8_sig").strip()
        if len(s) < 3:
            continue

        mo = ptn.search(s)
        if mo:
            fp.write(mo.group(1) + "\n")

    fp.close()


if __name__ == "__main__":
    main()
