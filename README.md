# clair-ubuntu
Repository used for storing files relevant to the CLAIR Ubuntu disentanglement project. Implementation of perceptron models for use on the ubuntu dataset can be found here: https://github.com/jpeper/irc-perceptron

**raw_data_processing.py**  
	Handles file processing and uses bag of words model to perform clustering of messages. Also does very primitive data annotation.   
        Usage: Specify the input filename as a command line argument 
	While running program the user will be given the option of performing kmeans, mean shift or spectral clustering and will be prompted at that time to enter the values of any relevant parameters.  
	For more information on clustering methods, see the following: http://scikit-learn.org/stable/modules/clustering.html

**basicstats.py**  
	Program which calculates basic statistics for a file from the ubuntu dataset  
	Usage: Specify the input filename as a command line argument

Example files from Ubuntu dataset:  
**ubuntu_small_sample.txt**   
small snippet (~30 messages) from Ubuntu logs  
**ubuntu_medium_sample.txt**    
moderately-sized (~170 messages) file containing dialogue from ubuntu irc chat  
**ubuntu_large_sample.txt**  
large (~4000 messages) file from Ubuntu logs  


