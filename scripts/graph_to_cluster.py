#!/usr/bin/env python3

from __future__ import print_function

import argparse
import logging
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a conversation graph to a set of connected components (i.e. threads).')
    args = parser.parse_args()

    # Simple, but slow implementation (should use a disjoint-set)
    clusters = []
    for line in sys.stdin:
        parts = line.strip().split()
        nums = set([int(p) for p in parts if p != '-'])

        to_merge = []
        for i, cluster in enumerate(clusters):
            if len(cluster.intersection(nums)) > 0:
                to_merge.append(i)

        # If we found no intersection, create a new set
        to_merge.sort(reverse=True)
        merged = set()
        for i in to_merge:
            merged.update(clusters[i])
            clusters.pop(i)
        merged.update(nums)
        clusters.append(merged)

    for cluster in clusters:
        print(" ".join([str(v) for v in cluster]))
