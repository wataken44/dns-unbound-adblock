#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" download_adblock.py


"""

import os
import re
import sys
import urllib.request

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) "}

OUTPUT_DIR = "blacklist/"

URLS = {
    "adguard-base": "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt",
    "adguard-mobile-ads": "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt",
    "adguard-japanese": "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/JapaneseFilter/sections/adservers.txt",
    "easylist": "https://easylist.to/easylist/easylist.txt",
}


def main():
    os.chdir(BASE_DIR)

    for name, url in URLS.items():
        req = urllib.request.Request(url, headers=HEADERS)
        res = None

        try:
            res = urllib.request.urlopen(req)
        except Exception as e:
            print(e)
            return

        ptn = re.compile("^\|\|([^/$]*)\^")

        fp = open(OUTPUT_DIR + name + ".txt", "w")

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
