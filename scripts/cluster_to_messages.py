#!/usr/bin/env python3

from __future__ import print_function

import argparse
import logging
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a conversation graph to a set of connected components (i.e. threads).')
    parser.add_argument('raw_data', help='File containing the raw logs')
    args = parser.parse_args()

    clusters = []
    for line in sys.stdin:
        nums = [int(v) for v in line.strip().split()]
        nums.sort()
        clusters.append(nums)

    text = []
    for line in open(args.raw_data):
        text.append(line.strip())

    for cluster in clusters:
        print(cluster)
        for num in cluster:
            print(text[num])
        print()
