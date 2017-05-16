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

    # Cohen's Kappa
    a, b, c, d = 0, 0, 0, 0
    max_pos = max(max([max(pair) for pair in pairs0]), max([max(pair) for pair in pairs1]))
    for i in range(max_pos):
        for j in range(i):
            if (i, j) in pairs0:
                if (i, j) in pairs1: a += 1
                else: b += 1
            else:
                if (i, j) in pairs1: c += 1
                else: d += 1
    total = a + b + c + d
    pO = (a + d) / total
    marginalA = (a + b) * (a + c) / total
    marginalB = (c + d) * (b + d) / total
    pE = (marginalA + marginalB) / total
    kappa = (pO - pE) / (1 - pE)

    # Harmonic mean of the two values for how many we had in common
    common = len(pairs0.intersection(pairs1))
    val0 = 100 * common / len(pairs0)
    val1 = 100 * common / len(pairs1)
    f1 = 2 * val0 * val1 / (val0 + val1)

    print("F1    {:.2f}   from {:.2f} {:.2f}".format(f1, val0, val1))
    print("Kappa {:.3f}".format(kappa))
