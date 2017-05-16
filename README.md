# clair-ubuntu
Repository used for storing files relevant to the clair unbuntu project.
Created on 2016-10-20.

raw_data_processing.py
	Handles file processing and uses bag of words model to perform clustering of messages. Also does very primitive data annotation. 
    Specify the input filename as a command line argument

basicstats.py
	Program which calculates basic statistics for a file from the ubuntu dataset
	Specify the input filename as a command line argument

Example files form ubuntu dataset:
ubuntu_small_sample.txt
	small snippet (~30 messages) from ubuntu logs
ubuntu_medium_sample.txt
	moderately-sized (~170 messages) file containing dialogue from ubuntu irc chat
2016-10-18_ubuntu.txt
	large (~4,000 messages) file containing entirety of messages from 
	main ubuntu irc channel on October 18th, 2016

