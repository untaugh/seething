#!/usr/bin/python3

import sys
import argparse
from pathlib import Path

sys.path.extend(['../seething'])
import parse

parser = argparse.ArgumentParser(description='Parse binary for debug symbols.')
parser.add_argument('objfile')
args = parser.parse_args()


json = parse.objToJson(args.objfile, skipdashed=False)

p = Path(args.objfile)

with Path('%s.json' % (p.name)).open('w') as f:
    f.write('data = \'')
    f.write(json)
    f.write('\';')

