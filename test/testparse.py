#!/usr/bin/python3

import sys

sys.path.extend(['../seething'])

import parse

parse.parseJson('test.c', 'seething.json')

