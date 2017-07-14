#!/usr/bin/env python3

import sys
import random

class Stat:
    def __init__(self, line):
        ### ubuntu/2008/08/2008-08-03.txt:00am 71 595 5 42.35294117647059 5637
        fields = line.strip().split()
        self.name = fields[0]
        self.users = int(fields[1])
        self.msgs = int(fields[2])
        self.directed = float(fields[4])

    def __repr__(self):
        return "{} u:{} m:{} %:{}".format(self.name, self.users, self.msgs, self.directed)

stats = []
for line in sys.stdin:
    stats.append(Stat(line))

def get_samples(data, name, value_function, parts=4, per_part=4):
    data.sort(key = value_function)
    samples = []
    for i in range(parts):
        count = 0
        while count < per_part:
            lower = i * len(data) // parts
            upper = (i + 1) * len(data) // parts
            sample = data[random.randint(lower, upper)]
            if '2014' in sample.name:
                pass
            elif '2015' in sample.name:
                pass
            elif '2016' in sample.name:
                pass
            elif '2017' in sample.name:
                pass
            else:
                count += 1
                samples.append(sample)
                print(name, i * 100 // parts, sample)

    return sample

# Do the general case

get_samples(stats, "Users", lambda x: x.users)
get_samples(stats, "Messages", lambda x: x.msgs)
get_samples(stats, "Directed", lambda x: x.directed)
