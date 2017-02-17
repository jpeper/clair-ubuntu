#!/usr/bin/env python3

import sys

for line in sys.stdin:
    parts = line.strip().split()
    filename = parts[2].split(':')[0]
    time = parts[2].split(':')[1]
    hour = time[:2]
    half_of_day = time[2:4]

    outname = filename.split('/')[-1][:-4] +"-"+ hour
    if half_of_day == 'am':
        outname += "-first.txt"
    else:
        outname += "-second.txt"
    out = open(outname, 'w')
    use = False
    part_of_day = "am"
    seen_hours = set()
    chour = None

    last_100 = []
    for line in open(filename):
        if line[0] == '[':
            thour = line[1:3]
            if thour != chour:
                chour = thour
                if thour in seen_hours:
                    part_of_day = "pm"
                seen_hours.add(thour)

        if line.startswith("="):
            if use:
                print(line.strip(), file=out)
        else:
            if line.startswith("["+hour):
                if half_of_day == part_of_day:
                    if not use:
                        print('\n'.join(last_100), file=out)
                        use = True
                    print(line.strip(), file=out)
            else:
                use = False

        last_100.append(line.strip())
        if len(last_100) > 100:
            last_100.pop(0)

    out.close()

