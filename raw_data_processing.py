import re
import operator
import pdb

class Post:    
    # constructor
    def __init__(self, userid, message, timeid):
    	
    	# member variables
    	self.userid = userid
    	self.message = message
    	self.timeid = timeid

    def __str__(self):
    	return 'User ID: ' + str(self.userid) + '\nMessage: ' + ' '.join(self.message) + "\nTimeID: " + str(self.timeid) + '\n'

    def get_message(self):
    	return self.message  

    def get_userid(self):
    	return self.userid

    def get_timeid(self):
    	return self.timeid

    
# create dictionary to hold mappings to user id's
user_aliases = {}
# list to store Post objects
entries = []

newuserid = 0
timestamp = 0

with open('ubuntu_small_sample.txt', 'r') as myfile:

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
					user_aliases[userid] = newuserid
					newuserid += 1

				# tokenize post body and store strings in list
				current_entry = re.findall(r'\[.+?\]\s<.+?>\s(.*)', line)			
				split = current_entry[0].split()
				# add object storing current comment's information to data list
				bob = Post(user_aliases[userid], split, timestamp)
				entries.append(bob)
				timestamp += 1

# prints summary of each entry	
for post in entries:
	print post

