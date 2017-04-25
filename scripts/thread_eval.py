#!/usr/bin/env python3

# For the definition of the metric, see https://en.wikipedia.org/wiki/Variation_of_information

from __future__ import print_function

import argparse
import math
import sys

def read_clusters(filename):
    ans = {}
    cfile = ""
    for line in open(filename):
        if ':' in line:
            cfile = ':'.join(line.split(':')[:-1])
            line = line.split(":")[-1]
        cluster = {int(v) for v in line.split()}
        ans.setdefault(cfile, []).append(cluster)
    return ans

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the Variation of Information metric for two clusters.')
    parser.add_argument('gold', help='File containing the gold clusters, one per line. If a line contains a ":" the start is considered a filename')
    parser.add_argument('auto', help='File containing the gold clusters, one per line. If a line contains a ":" the start is considered a filename')
    args = parser.parse_args()

    auto = read_clusters(args.auto)
    gold = read_clusters(args.gold)

    scores = {}
    points = {}
    # Output only in one or the other
    for filename in auto:
        for cluster in auto[filename]:
            points.setdefault(filename, set()).update(cluster)
        if filename not in gold:
            scores[filename] = 0.0
    for filename in gold:
        for cluster in gold[filename]:
            points.setdefault(filename, set()).update(cluster)
        if filename not in auto:
            scores[filename] = 0.0

    total_points = 0
    for filename in points:
        total_points += len(points[filename])

    # Files with both
    for filename in gold:
        if filename in auto:
            scores[filename] = 0.0
            for cluster_g in gold[filename]:
                for cluster_a in auto[filename]:
                    p = len(cluster_g)
                    q = len(cluster_a)
                    r = len(cluster_a.intersection(cluster_g))
                    if r != 0:
                        to_add = - (r / total_points) * (math.log(r / p, 2) + math.log(r / q, 2))
                        scores[filename] += to_add

    max_score = math.log(total_points, 2)
    print('Worst score:', max_score, 'Total items:', total_points)
    print("VI, Normalised-VI, Filename (if given)")

    total = 0
    for filename in scores:
        max_score = math.log(len(points[filename]), 2)
        total += scores[filename]
        print(scores[filename], scores[filename] / max_score, filename)

    if len(scores) > 1:
        max_score = math.log(total_points, 2)
        print(total, total / max_score, 'all files combined')
