#!/usr/bin/env python3

import sys

def get_target(word, users, step):
    if word[-1] in ':,':
        word = word[:-1]

    # Only count it if the user appeared recently
    if step - users.get(word, -1000) < 200:
        return word
    else:
        return None

def save_stats(stats, filename, ctime, msg_per_user, msg_with_target, words):
    key = filename.strip() +':'+ ctime
    stats[key] = (msg_per_user, msg_with_target)

    counts = msg_per_user
    targets = msg_with_target

    n_users = len(counts)

    n_msg = 0
    sorted_counts = []
    for user in counts:
        n_msg += counts[user]
        sorted_counts.append(counts[user])

    perc = 100 * targets / n_msg

    sorted_counts.sort()
    median = None
    if len(sorted_counts) > 0:
        median = sorted_counts[len(sorted_counts) // 2]

    print(key, n_users, n_msg, median, perc, words)



if __name__ == '__main__':
    stats = {}
    users = {}
    step = 0
    cur_msg_per_user = {}
    cur_msg_with_target = 0
    cur_words = 0
    for filename in sys.stdin:
        ctime = None
        part_of_day = "am"
        seen_hours = set()
        chour = None
        for line in open(filename.strip(), encoding='latin-1'):
            if line[0] == '[':
                hour = line[1:3]
                if hour != chour:
                    chour = hour
                    if hour in seen_hours:
                        part_of_day = "pm"
                    seen_hours.add(hour)

            if line[0] == '=':
                if 'is now known as' in line:
                    oldname = line.strip().split()[1]
                    newname = line.strip().split()[-1]
                    users[newname] = step
                    if oldname in cur_msg_per_user:
                        cur_msg_per_user[newname] = cur_msg_per_user[oldname]
                        cur_msg_per_user.pop(oldname, None)
            elif line[0] == '[':
                step += 1
                fields = line.strip().split()

                time = fields[0][1:-4] + part_of_day
                if time != ctime:
                    # Save stats
                    if ctime is not None:
                        save_stats(stats, filename, ctime, cur_msg_per_user,
                                cur_msg_with_target, cur_words)
                    # Reset
                    cur_msg_per_user = {}
                    cur_msg_with_target = 0
                    cur_words = 0
                    ctime = time

                user = fields[1][1:-1]
                users[user] = step
                cur_msg_per_user[user] = cur_msg_per_user.get(user, 0) + 1
                cur_words += len(fields) - 2

                if len(fields) > 2:
                    target = get_target(fields[2], users, step)
                    if target is not None:
                        cur_msg_with_target += 1

        # Save stats
        if ctime is not None:
            save_stats(stats, filename, ctime, cur_msg_per_user,
                    cur_msg_with_target, cur_words)

