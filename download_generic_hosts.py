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
    "stevenblack": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "hagzi": "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/hosts/pro.txt",
}

WHITELIST = [
    "broadcasthost",
    "ip6-allhosts",
    "ip6-allnodes",
    "ip6-allrouters",
    "ip6-localhost",
    "ip6-localnet",
    "ip6-loopback",
    "ip6-mcastprefix",
    "local",
    "localhost",
    "localhost.localdomain",
]


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
            continue

        fp = open(BASE_DIR + "blacklist/" + key + ".txt", "w")

        for line in res:
            s = line.decode("utf-8").strip()
            if s == "" or s[0] == "#" or (s in WHITELIST):
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
