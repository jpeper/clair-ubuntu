#!/usr/bin/env python3

from __future__ import print_function

import argparse
import logging
import sys

def get_pairs(filename):
    pairs = set()
    for line in open(filename):
        parts = line.strip().split()
        src = int(parts[0])
        for part in parts[2:]:
            antecedent = int(part)
            pairs.add((src, antecedent))
    return pairs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare annotations of conversation graphs')
    parser.add_argument('file0', help='File containing annotations')
    parser.add_argument('file1', help='File containing annotations')
    args = parser.parse_args()

    pairs0 = get_pairs(args.file0)
    pairs1 = get_pairs(args.file1)

    common = len(pairs0.intersection(pairs1))

    print(common, len(pairs0), len(pairs1), common / max(len(pairs0), len(pairs1)))
