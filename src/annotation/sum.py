#!/usr/bin/env python3

import sys

sums = {}
for line in sys.stdin:
    parts = line.strip().split()
    num = int(parts[-1])
    name = ' '.join(parts[:-1])
    if name not in sums:
        sums[name] = 0
    sums[name] += num

for name in sums:
    print(name, sums[name])
