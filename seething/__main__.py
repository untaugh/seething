#!/usr/bin/python3

import core
import argparse

parser = argparse.ArgumentParser(description='Visualize C code.')
parser.add_argument('path')
args = parser.parse_args()

core.startServer(args.path)
