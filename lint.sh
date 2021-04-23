#!/bin/sh
set -ex

# stop the build if there are Python syntax errors or undefined names
flake8 *.py cwa --count --select=E9,F63,F7,F82 --show-source --statistics

# The GitHub editor is 127 chars wide
flake8 *.py cwa --count --max-complexity=10 --max-line-length=127 --statistics --exclude cwa/cwa_pb2.py
