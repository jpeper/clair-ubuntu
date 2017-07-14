#!/usr/bin/env python3

import sys

nums = {}
highest = 0
for line in sys.stdin:
    parts = line.strip().split()
    source = int(parts[0])
    targets = {int(v) for v in parts[2:]}
    nums[source] = targets
    if source > highest:
        highest = source

counts = {0: 0}
dists = {0: 0}
for i in range(101, highest + 1):
    if i not in nums:
        counts[0] += 1
    else:
        targets = nums[i]
        if len(targets) not in counts:
            counts[len(targets)] = 0
        counts[len(targets)] += 1
        for num in targets:
            dist = i - num
            if dist not in dists:
                dists[dist] = 0
            dists[dist] += 1

for dist in dists:
    print('dist', dist, dists[dist])
for count in counts:
    print('count', count, counts[count])
