#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" download_generic_hosts.py


"""

import os
import re
import sys
import urllib.request

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) "}
URLS = {
    "adaway": "https://adaway.org/hosts.txt",
    "warui": "https://warui.intaa.net/adhosts/hosts_lb.txt",
}


def main():
    os.chdir(BASE_DIR)

    hosts_ptn = re.compile(r"\d+\.\d+.\d+.\d+\s+(.*)")
    ip_ptn = re.compile(r"^\d+\.\d+\.\d+\.\d+$")

    for key, url in URLS.items():

        req = urllib.request.Request(url, headers=HEADERS)
        res = None

        try:
            res = urllib.request.urlopen(req)
        except Exception as e:
            print(e)

        fp = open(BASE_DIR + "blacklist/" + key + ".txt", "w")

        for line in res:
            s = line.decode("utf-8").strip()
            if s == "" or s.find("localhost") >= 0 or s[0] == "#":
                continue

            mo = hosts_ptn.search(s)
            if mo:
                d = mo.group(1)
                if ip_ptn.search(d):
                    pass
                else:
                    fp.write(d + "\n")

        fp.close()


if __name__ == "__main__":
    main()
