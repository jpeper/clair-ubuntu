import re
import operator
import pdb
import numpy
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import euclidean


class Post(object):    
    # constructor
    def __init__(self, userid, message_words, message, timeid):
    	
    	# member variables
    	self.userid = userid
    	self.message_words = message_words
    	self.message = message
    	self.timeid = timeid

    def __str__(self):
    	return 'User ID: ' + str(self.userid) + '\nMessage: ' + self.message + "\nTimeID: " + str(self.timeid) + '\n'

    def get_userid(self):
    	return self.userid

    def get_message_words(self):
    	return self.message_words

    def get_message(self):
    	return self.message      

    def get_timeid(self):
    	return self.timeid

    
# create dictionary to hold mappings to user id's
user_aliases = {}

# list to store Post objects
entries = []

newuserid = 0
timestamp = 0


with open('2016-10-18_ubuntu.txt', 'r') as myfile:

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
				bob = Post(user_aliases[userid], split, current_entry[0], timestamp)
				entries.append(bob)
				timestamp += 1




message_list = []
for posts in entries:
	message_list.append(posts.get_message())

vectorizer = CountVectorizer(analyzer = "word", binary = True, tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000) 
word_vec = vectorizer.fit_transform(message_list)

bin_matrix = word_vec.todense()
# print dimensions of binary frequency matrix
print (bin_matrix.shape)


vocab = vectorizer.get_feature_names()
#print (vocab)
num_clusters = 100
kmeans = KMeans(n_clusters = num_clusters)
kmeans.fit(bin_matrix)

bob = euclidean(bin_matrix[2,:], bin_matrix[3,:])
print (bob)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

#print (labels)
#print (centroids[2])

#print out like messages


for i in range(num_clusters):
	min_dist = 1000000000;
	min_index = 0;
	print ("Messages in cluster", i,':')
	for j in range(len(message_list)):
		if (labels[j] == i):
			if (euclidean(bin_matrix[j], centroids[i]) < min_dist):
				min_dist = euclidean(bin_matrix[j], centroids[i]) 
				min_index = j
			print (message_list[j])
	print ("\nCluster Medoid: ", message_list[min_index], '\n'*4)



