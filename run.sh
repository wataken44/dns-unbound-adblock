#!/bin/bash

python3 download_generic_hosts.py
python3 download_adblock.py
python3 download_280blocker.py
python3 create_unbound_conf.py
