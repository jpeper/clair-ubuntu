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
    for filename in ans:
        min_num = -1
        max_num = -1
        seen = set()
        for cluster in ans[filename]:
            this_min = min(cluster)
            this_max = max(cluster)
            seen.update(cluster)
            if min_num < 0 or this_min < min_num:
                min_num = this_min
            if max_num < 0 or this_max > max_num:
                max_num = this_max
        for num in range(min_num, max_num):
            if num not in seen:
                ans[filename].append({num})
    return ans

def variation_of_information(gold, auto):
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
    print('VI Worst score:', max_score, 'Total items:', total_points)
    print("VI, Normalised-VI, Filename (if given)")

    total = 0
    for filename in scores:
        max_score = math.log(len(points[filename]), 2)
        total += scores[filename]
        print(scores[filename], scores[filename] / max_score, filename)

    if len(scores) > 1:
        max_score = math.log(total_points, 2)
        print(total, total / max_score, 'all files combined')

def van_dongen(gold, auto):
    scores = {}
    points = {}
    # Output only in one or the other
    for filename in auto:
        total = 0
        for cluster in auto[filename]:
            points.setdefault(filename, set()).update(cluster)
            total += len(cluster)
        if filename not in gold:
            scores[filename] = 2 * len(points[filename])
    for filename in gold:
        for cluster in gold[filename]:
            points.setdefault(filename, set()).update(cluster)
        if filename not in auto:
            scores[filename] = 2 * len(points[filename])

    total_points = 0
    for filename in points:
        total_points += len(points[filename])

    max_score = 2 * total_points
    overall = max_score
    for filename in points:
        if filename in auto:
            score = 2 * len(points[filename])
            for cluster_g in gold[filename]:
                best = 0
                for cluster_a in auto[filename]:
                    r = len(cluster_a.intersection(cluster_g))
                    if r > best: best = r
                score -= best
                overall -= best
            for cluster_a in auto[filename]:
                best = 0
                for cluster_g in gold[filename]:
                    r = len(cluster_a.intersection(cluster_g))
                    if r > best: best = r
                score -= best
                overall -= best
            scores[filename] = score

    print('van dongen total items:', total_points)
    for filename in scores:
        print(scores[filename], scores[filename] / (2 * len(points[filename])), filename)
    if len(scores) > 1:
        print(overall, overall / max_score, "all")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the Variation of Information metric for two clusters.')
    parser.add_argument('gold', help='File containing the gold clusters, one per line. If a line contains a ":" the start is considered a filename')
    parser.add_argument('auto', help='File containing the gold clusters, one per line. If a line contains a ":" the start is considered a filename')
    args = parser.parse_args()

    auto = read_clusters(args.auto)
    gold = read_clusters(args.gold)

    variation_of_information(gold, auto)
    van_dongen(gold, auto)
