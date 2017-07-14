#!/usr/bin/env python3

import random

data = [
  ("2008-04-27-06-first.txt", 1068), ("2006-06-01-12-second.txt", 1036),
  ("2008-04-30-08-first.txt", 796), ("2006-06-05-12-second.txt", 748),
  ("2007-12-17-04-first.txt", 738), ("2007-06-04-10-second.txt", 731),
  ("2007-01-19-07-first.txt", 711), ("2007-07-03-06-second.txt", 645),
  ("2007-06-17-06-second.txt", 635), ("2006-08-23-03-first.txt", 628),
  ("2007-09-07-07-second.txt", 609), ("2007-08-19-01-first.txt", 594),
  ("2006-12-10-09-second.txt", 552), ("2008-06-03-11-first.txt", 529),
  ("2010-08-29-20-first.txt", 522), ("2011-04-28-09-first.txt", 502),
  ("2008-04-20-09-first.txt", 473), ("2012-05-20-16-first.txt", 454),
  ("2005-06-20-03-second.txt", 439), ("2009-03-25-11-first.txt", 439),
  ("2010-02-13-01-first.txt", 406), ("2009-01-05-11-first.txt", 405),
  ("2013-10-28-03-first.txt", 393), ("2012-11-30-14-first.txt", 379),
  ("2013-01-30-01-first.txt", 379), ("2013-02-24-02-first.txt", 373),
  ("2010-08-05-11-first.txt", 371), ("2013-09-12-11-first.txt", 350),
  ("2006-02-24-10-first.txt", 332), ("2012-02-03-20-first.txt", 322),
  ("2012-11-24-20-first.txt", 307), ("2012-05-04-04-first.txt", 302),
  ("2013-07-19-03-first.txt", 287), ("2013-05-19-22-first.txt", 271),
  ("2013-12-02-21-first.txt", 266), ("2005-07-25-11-first.txt", 264),
  ("2012-12-15-02-first.txt", 255), ("2005-02-08-02-second.txt", 249),
  ("2013-05-05-18-first.txt", 248), ("2013-05-07-02-first.txt", 240),
  ("2005-05-19-11-first.txt", 232), ("2012-06-02-18-first.txt", 231),
  ("2011-08-17-08-first.txt", 228), ("2013-08-30-11-first.txt", 221),
  ("2013-07-10-23-first.txt", 220), ("2013-10-11-07-first.txt", 167),
  ("2013-01-11-13-first.txt", 161), ("2013-10-04-12-first.txt", 156),
]

groups = []
while len(data) > 0:
    cgroup = []
    total = 0
    pos = 0
    while pos < len(data) and total < 900:
        num = data[pos][1] - 100
        if total + num < 1100:
            cgroup.append(data.pop(pos))
            total += num
        else:
            pos += 1
    groups.append((total, ' '.join(map(lambda x: x[0], cgroup))))

groups.sort(key=lambda x: random.random())
for group in groups:
    print(group[0], group[1])
