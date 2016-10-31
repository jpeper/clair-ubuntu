import re
import operator
import pdb


# create dictionary to map 
user_aliases = {}

class Post:
    
    # constructor
    def __init__(self, userid, message, timeid):
    	
    	# member variables
    	self.userid = userid
    	self.message = message
    	self.timeid = timeid

    def __str__(self):
    	return 'User ID: ' + str(self.userid) + '\nMessage: ' + ' '.join(self.message) + "\nTimeID: " + str(self.timeid)

    def get_message(self):
    	return self.message   
    

entries = []
# open data file
newuserid = 0
timestamp = 0
with open('ubuntu_annotated_sample.txt', 'r') as myfile:

	for line in myfile:	
		
		# if name is changed on line
		if (re.search(r'^===', line)):			
			
			# extract old and new name
			names = re.search(r'=== (.+?) is now known as (.*)\r?',line)
			old_name = names.group(1) 
			new_name = names.group(2)
			# if old name didn't exist in this file, 
			# add new one to user alias dictionary
			if not old_name in user_aliases:
				user_aliases[new_name] = newuserid
				newuserid += 1
			# otherwise, set the id of the new alias 
			# to the id of the old name
			else:
				user_aliases[new_name] = user_aliases[old_name]

		# if line contains a normal post, add username to dictionary
		else:
			current_line = re.search(r'\[.+?\]\s<(.+?)>', line)
			if current_line:

				userid = current_line.group(1)
				# if user has not posted before, assign them a user id
				if not userid in user_aliases:
					print newuserid
					user_aliases[userid] = newuserid
					newuserid += 1

				# tokenize post body
				current_entry = re.findall(r'\[.+?\]\s<.+?>\s(.*)', line)			
				split = current_entry[0].split()
				# add object storing current comment's information to data list
				bob = Post(user_aliases[userid], split, timestamp)
				entries.append(bob)
				timestamp += 1
	
for entry in entries:
	
	print entry

# print sorted(user_aliases.items(), key=operator.itemgetter(1))

"""
# find all usernames and store in list of strings



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
"""