#!/usr/bin/python3

import sys

sys.path.extend(['../seething'])

import parse

print(parse.getJsFuncDefs('test.c'))
