#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" download_280blocker.py


"""

import datetime
import os
import sys
import urllib.request

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) "}
OUTPUT = "blacklist/280blocker.txt"
URL = "https://280blocker.net/files/280blocker_domain_%04d%02d.txt"


def main():
    os.chdir(BASE_DIR)

    now = datetime.datetime.now()

    year = now.year
    month = now.month

    for i in range(3):

        url = URL % (year, month)
        req = urllib.request.Request(url, headers=HEADERS)
        res = None

        try:
            res = urllib.request.urlopen(req)
        except Exception as e:
            print(e)
            year, month = prev_month(year, month)
            continue

        fp = open(OUTPUT, "w")
        fp.write(res.read().decode("utf-8"))
        fp.close()

        break


def prev_month(year, month):
    if month == 1:
        return year - 1, 12
    else:
        return year, month


if __name__ == "__main__":
    main()
