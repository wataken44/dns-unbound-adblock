#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" download_280blockaer.py


"""

import os
import sys

BASE_DIR=os.path.abspath(os.path.dirname(__file__)) + "/"

def main():
    os.chdir(BASE_DIR)
    os.system("wget -q 'https://280blocker.net/files/280blocker_domain.txt' -O blacklist/280blocker_domain.txt")

if __name__ == "__main__":
    main()
