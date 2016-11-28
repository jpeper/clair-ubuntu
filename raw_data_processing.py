import re
import operator
import pdb
import numpy
import pickle
import marshal
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import euclidean
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MeanShift
from sklearn.preprocessing import normalize

input_file = "ubuntu_medium_sample.txt"

class Post(object):    
    # constructor
    def __init__(self, username, userid, message_words, message, postid, raw_line, responding_to_id = None):
    	
    	# member variables
    	# stores name of user
    	self.username = username
    	# stores id assigned to user and their aliases
    	self.userid = userid
    	# stores list of strings which contains every 'word' in the message
    	self.message_words = message_words
    	# string of message body
    	self.message = message
    	# stores id number assigned to post
    	self.postid = postid
    	# stores id number of the post that current post 
    	# is responding to
    	self.responding_to_id = responding_to_id
    	# stores actual line of raw input corresponding to current post
    	self.raw_line = raw_line

    def __str__(self):
    	return 'Username: ' + self.username + ', User ID: ' + str(self.userid) + ', Post ID: ' + str(self.postid) + ', Responding to Post ID: ' + str(self.responding_to_id) + '\nMessage: ' + self.message 
    
    def get_username(self):
    	return self.username

    def get_userid(self):
    	return self.userid

    def get_message_words(self):
    	return self.message_words

    def get_message(self):
    	return self.message      

    def get_postid(self):
    	return self.postid

    def set_responding_to_id(self, id_in):    	
    	self.responding_to_id = id_in  
    	
    def get_responding_to_id(self):
    	return self.responding_to_id

    def get_raw_line(self):
    	return self.raw_line

    # returns annotated representation of message suitable for output to file
    def get_annotated(self):
    	return '(' + str(self.postid) + ')' + ' (' + str(self.responding_to_id) + ') ' + self.raw_line

    
# create dictionary to hold mappings to user id's
user_aliases = {}

# list to store Post objects
entries = []

# file processing
def file_processing(file_in):

	global user_aliases
	global entries
	newuserid = 0
	post_num = 0

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
				username = current_line.group(1)
				# if user has not posted before, assign them a user id
				if not username in user_aliases:
					user_aliases[username] = newuserid
					newuserid += 1

				# tokenize post body and store strings in list
				current_entry = re.findall(r'\[.+?\]\s<.+?>\s(.*)', line)	
				split = current_entry[0].split()
				# add object storing current comment's information to data list
				new_post = Post(username, user_aliases[username], split, current_entry[0], post_num, line)
				entries.append(new_post)
				post_num += 1

def annotate(entries_list):

	# prompt user for starting position, number of messages to display, and output filename  
    start_position = int(input("There are " + str(len(entries)) + " messages in this file. Pick starting message in range [0," + str(len(entries)) + ")\n" ))
    num_messages = int(input("How many past messages would you like to display?\n"))
    filename = input("Please enter annotated output destination filename:\n")
    saveFile = open(filename, 'w')

    doAnnotation = True
    index = start_position

    # while user wants to do annotation of messages in list
    while ((doAnnotation == True) and (index < len(entries))):

    	# display previous messages with corresponding value 
    	num_entries_to_print = min(num_messages, index)
    	print ("\nPREVIOUS MESSAGES")
    	for j in range(num_entries_to_print):
    		print ('[',j,']\t', entries_list[index - num_entries_to_print + j].get_annotated().rstrip())
    	print ('\n')

    	# display current message    	
    	print ('CURRENT MESSAGE:\n' + entries_list[index].get_annotated() + '\n')

    	# prompt input from user
    	valid_input = False
    	while (valid_input == False):

    		current_val = int(input("Select previous message in dialogue. If none exists, enter -1. Enter -2 to exit annotation.\n"))
    		
    		# if 'end of annoation' sentinel value is entered, break from input
    		if (current_val == -2):
    			doAnnotation = False
    			break

    		# create new dialogue 
    		elif (current_val == -1):
    			break

    		# link current message to previous message
    		elif ((current_val >= 0) and (current_val < num_entries_to_print)):
    			entries_list[index].set_responding_to_id(entries_list[index - num_entries_to_print + current_val].get_postid())
    			valid_input = True

    		# if invalid input, prompt user to enter correct value
    		else:
    			print ("Invalid input. Please try again")

    	# print line to keep annotation of each message distinct    	
    	print ('_'*120)

    	# if annotation is over, exit function
    	if (doAnnotation == False):
    		break;

    	# write annotated object to line in output file	
    	saveFile.write(entries_list[index].get_annotated())

    	# increment index
    	index += 1

    # close output file
    saveFile.close()

    print ("\nEnd of Annotation\n")

# KMEANS
def tokenize(message):
	split_message = message.split()
	return split_message

def clustering(entries_list):

	# determine number of clusters
	k = int(input("Number of messsages = " + str(len(entries)) + ". How many clusters would you like? Enter value in range (0," + str(len(entries)) + "]\n"))

	message_list = []
	for posts in entries_list:
		message_list.append(posts.get_username() + " " + posts.get_message())

	#vectorizer = CountVectorizer()
	vectorizer = CountVectorizer(analyzer='word',binary=True,tokenizer=tokenize,preprocessor=None,stop_words=None) 
	word_vec = vectorizer.fit_transform(message_list)
	bin_matrix = normalize(word_vec)

	bin_matrix = bin_matrix.todense()
	
	'''
	for messages in entries:
	for words in messages.message_words:
		print (words)
	'''

	# print dimensions of binary frequency matrix
	print ("Dimensions of matrix:",bin_matrix.shape)


	vocab = vectorizer.get_feature_names()
	print (vocab)
	kmeans = KMeans(n_clusters = k)
	kmeans.fit(bin_matrix)

	dist = euclidean(bin_matrix[2,:], bin_matrix[3,:])
	

	centroids = kmeans.cluster_centers_
	labels = kmeans.labels_

	for i in range(k):
		min_dist = 1000000000000;
		min_index = 0;

		print ("\n"*2, "\nMESSAGES IN CLUSTER",i,':')
		for j in range(len(message_list)):
			if (labels[j] == i):
				if (euclidean(bin_matrix[j], centroids[i]) < min_dist):
					min_dist = euclidean(bin_matrix[j], centroids[i]) 
					min_index = j
				print (message_list[j])
		print ("\nCLUSTER " + str(i) + " MEDOID:\n" + message_list[min_index])
		print ("_"*100)


'''
# MEAN SHIFT
def clustering(entries_list):

	# determine number of clusters
	#k = int(input("Number of messsages = " + str(len(entries)) + ". How many clusters would you like? Enter value in range (0," + str(len(entries)) + "]\n"))

	message_list = []
	for posts in entries_list:
		message_list.append(posts.get_message())


	vectorizer = CountVectorizer(analyzer = "word", binary = True, tokenizer = None, preprocessor = None, stop_words = None) 
	word_vec = vectorizer.fit_transform(message_list)

	bin_matrix = word_vec.todense()
	# print dimensions of binary frequency matrix
	print ("Dimensions of matrix:",bin_matrix.shape)


	vocab = vectorizer.get_feature_names()
	#print (vocab)
	kmeans = MeanShift()
	kmeans.fit(bin_matrix)


	dist = euclidean(bin_matrix[2,:], bin_matrix[3,:])
	

	centroids = kmeans.cluster_centers_
	labels = kmeans.labels_
	

	for i in range(centroids.shape[0]):
		min_dist = 1000000000;
		min_index = 0;

		print ("\n"*2, "\nMESSAGES IN CLUSTER",i,':')
		for j in range(len(message_list)):
			if (labels[j] == i):
				if (euclidean(bin_matrix[j], centroids[i]) < min_dist):
					min_dist = euclidean(bin_matrix[j], centroids[i]) 
					min_index = j
				print (message_list[j])
		print ("\nCLUSTER " + str(i))
		print ("_"*100)
'''

'''
# SPECTRAL CLUSTERING
def clustering(entries_list):

	# determine number of clusters
	k = int(input("Number of messsages = " + str(len(entries)) + ". How many clusters would you like? Enter value in range (0," + str(len(entries)) + "]\n"))

	message_list = []
	for posts in entries_list:
		message_list.append(posts.get_message())


	vectorizer = CountVectorizer(analyzer = "word", binary = True, tokenizer = None, preprocessor = None, stop_words = None) 
	word_vec = vectorizer.fit_transform(message_list)

	bin_matrix = word_vec.todense()
	# print dimensions of binary frequency matrix
	print ("Dimensions of matrix:",bin_matrix.shape)


	vocab = vectorizer.get_feature_names()
	#print (vocab)
	kmeans = SpectralClustering(k)
	kmeans.fit(bin_matrix)

	labels = kmeans.labels_

	for i in range(k):
		for j in range(len(message_list)):
			if (labels[j] == i):
				print (message_list[j])
		print ("\nCLUSTER ", i)
		print ("_"*100, "\n")
'''

	

'''
	kmeans.fit(bin_matrix)

	dist = euclidean(bin_matrix[2,:], bin_matrix[3,:])
	

	centroids = kmeans.cluster_centers_
	labels = kmeans.labels_

	for i in range(k):
		min_dist = 1000000000;
		min_index = 0;

		print ("\n"*2, "\nMESSAGES IN CLUSTER",i,':')
		for j in range(len(message_list)):
			if (labels[j] == i):
				if (euclidean(bin_matrix[j], centroids[i]) < min_dist):
					min_dist = euclidean(bin_matrix[j], centroids[i]) 
					min_index = j
				print (message_list[j])
		print ("\nCLUSTER " + str(i) + " MEDOID:\n" + message_list[min_index])
		print ("_"*100)
	'''


# INPUT FILE
myfile = open(input_file, 'r')
file_processing(myfile)

# run annotation function if requested
do_annotation = input("Would you like to do annotation? (yes/no)\n")
if do_annotation == 'yes':
	annotate(entries)

# run clustering fuction if requested
do_clustering = input ("Would you like to do clustering? (yes/no)\n")
if do_clustering == 'yes':
	clustering(entries)













