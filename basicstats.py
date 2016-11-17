import re

input_file = 'ubuntu_small_sample.txt'
with open(input_file, 'r') as myfile:
    data=myfile.read().replace('\n', '')

post_username = re.findall(r'\[.+?\]\s<(.+?)>', data)

user_frequency = dict()
for user in post_username:
 	user_frequency[user] = user_frequency.get(user, 0) + 1

print "\nNumber of Posts:", len(post_username), "\n"
print "Number of Users:", len(user_frequency), "\n"

print "Users sorted alphabetically:"
print "Frequency\t", "Username" 
for i in sorted(user_frequency):
	print user_frequency[i], "\t\t", i

print "\nUsers sorted by post frequency:"
print "Frequency\t", "Username" 
for i in sorted(user_frequency, key=user_frequency.get):
	print user_frequency[i], "\t\t", i
