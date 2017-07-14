#!/usr/bin/env python3

import sys

for line in open(sys.argv[1]):
    ours, theirs = line.strip().split()
    name = ours.split(".txt")[0]

    their_nums = set()
    for line in open(theirs):
        nums = {int(v) for v in line.strip().split() if int(v) > 100}
        their_nums.update(nums)
        if len(nums) > 0:
            print("Theirs", name +":"+ ' '.join([str(n) for n in nums]))

    done = set()
    for line in open(ours):
        nums = {int(v) for v in line.strip().split() if int(v) in their_nums}
        done.update(nums)
        if len(nums) > 0:
            print("Ours", name +":"+ ' '.join([str(n) for n in nums]))
    for num in their_nums:
        if num not in done:
            print("Ours", name +":"+ str(num))
