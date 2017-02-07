#!/usr/bin/env python3

import argparse
import glob

def read_file(filename):
    # Determine offset
    number = int(filename.split("rawLogtxtpart")[1].split("txt")[0])
    offset = 40 * number

    ans = {}
    data = eval(open(filename).read())
    for pair in data:
        key = (pair[0] + offset, pair[1] + offset)
        ans[key] = ans.get(key, 0) + 1
    return ans

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool to combine mturk annotations.')
    parser.add_argument('directory', help='Directory containing files to combine')
    args = parser.parse_args()

    all_data = {}
    links = {}
    for name in glob.glob(args.directory +"/*"):
        data = read_file(name)
        for key in data:
            all_data[key] = all_data.get(key, 0) + data[key]
            links.setdefault(key[1], set()).add(key[0])

    for num in links:
        print(num, '-', ' '.join([str(v) for v in links[num]]))
