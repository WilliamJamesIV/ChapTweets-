# Author: Liliana Hernandez and William James
# Version 1.1

import twitter
import json
import csv
import smtplib
from prettytable import PrettyTable
from urllib import unquote

CONSUMER_KEY = 'qqC37cuCTO61c3VrMDxqavdZF'
CONSUMER_SECRET = 'oRCLdjKTnuwYfvQX37mkLNmt0zHUxN4pKwnWuOI9fxYQukBVLa'
OAUTH_TOKEN = '3161359674-d5BHQEKUIspJUb4gtwmvH6dM08k6TM3kh7JEnWG'
OAUTH_TOKEN_SECRET = 'lvKRXJjYx7blVjuSoOuCi9hqqbPcugGnCq2GxfKhXLNed'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

def menu():
	print
	print "1. View tweets about Chapman" #
	print "2. View top trends at Chapman" #
	print "3. View tweets that use #Chapman" #
	print "4. View tweets that use #CU" #
	print "5. View tweets that use #Fenestra" #
	print "6. Perform a sentiment analysis between Chapman and Redlands" #
	print "7. Perform a sentiment analysis between two words of your liking" #
	print "8. Get average length of tweets that mention Chapman" #
	print "9. Get average number of hashtags used in tweets that mention Chapman" #
	print "10. Print out information about recent tweets" # 
	print "11. Perform a sentiment analysis on a word" #
	print "12. Search for a term and Export the Info to a CSV file" #
	print "13. Return Most popular retweets with Chapman University in table view" #
	print "14. Exit"
	print

def sentimentAnalysis(q1,q2):
	count = 1000

	search_results1 = twitter_api.search.tweets(q=q1, count=count)
	search_results2 = twitter_api.search.tweets(q=q2, count=count)

	statuses1 = search_results1['statuses']
	statuses2 = search_results2['statuses']

	# Iterate through 5 more batches of results by following the cursor

	for _ in range(5):
		try:
			next_results = search_results1['search_metadata']['next_results']
		except KeyError, e: # No more results when next_results doesn't exist
			break
		kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

		search_results1 = twitter_api.search.tweets(**kwargs)
		statuses1 += search_results1['statuses']

	for _ in range(5):
		try:
			next_results = search_results2['search_metadata']['next_results']
		except KeyError, e: # No more results when next_results doesn't exist
			break
		kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

		search_results2 = twitter_api.search.tweets(**kwargs)
		statuses2 += search_results2['statuses']

	status_texts1 = [ status['text'] for status in statuses1 ]
	status_texts2 = [ status['text'] for status in statuses2 ]

	# Compute a collection of all words from all tweets
	words1 = [ w
			for t in status_texts1
				for w in t.split() ]
	words2 = [ w
			for t in status_texts2
				for w in t.split() ]

	#sentiment analysis first term
	sent_file1 = open('AFINN-111.txt')

	scores1 = {}
	for line in sent_file1:
		term, score  = line.split("\t")
		scores1[term] = int(score)

	score1 = 0
	for word in words1:
		uword = word.encode('utf-8')
		if uword in scores1.keys():
			score1 = score1 + scores1[word]

	result1 = q1 + " has a sentiment analysis of " + str(score1)
	print result1

	sent_file1.close()

	#sentiment analysis second term
	sent_file2 = open('AFINN-111.txt')
	scores2 = {}
	for line in sent_file2:
		term, score  = line.split("\t")
		scores2[term] = int(score)

	score2 = 0
	for word in words2:
		uword = word.encode('utf-8')
		if uword in scores2.keys():
			score2 = score2 + scores2[word]

	result2 = q2 + " has a sentiment analysis of " + str(score2)
	print result2
	sent_file2.close()

	if(score1 > score2):
		result3 = q1+ " has the most positive sentiment"
		print result3
	else:
		result3 = q2+ " has the most positive sentiment"
		print result3

	return result1+"\n"+result2+"\n"+result3


def averageLength():
	count = 1000
	search_results = twitter_api.search.tweets(q="Chapman University", count=count)
	statuses = search_results['statuses']
	status_texts = [ status['text']
		for status in statuses ]
	words = [ w
		for t in status_texts
			for w in t.split() ]

	average = len(words)/float(len(status_texts))
	result = "Average length of tweets that mention Chapman University is " + str(average) + " words"
	print result
	return result

def averageHashtags():
	count = 1000
	search_results = twitter_api.search.tweets(q="Chapman University", count=count)
	statuses = search_results['statuses']
	status_texts = [ status['text']
		for status in statuses ]
	hashtags = [ hashtag['text']
		for status in statuses
			for hashtag in status['entities']['hashtags'] ]

	average = len(hashtags) / float(len(status_texts))
	result = "Average number of hashtags used in tweets that mention Chapman University is " + str(average) + " hastags"
	print result
	return result


#prints out text, screen names and hashtags for most recent tweets

def printTwitterInfo(q):

	from urllib import unquote
	count = 500

	search_results = twitter_api.search.tweets(q=q, count=count,result_type='recent') # adding result_type='recent' for recent tweets

	statuses = search_results['statuses']

	# Iterate through 5 more batches of results by following the cursor
        #try changing 5 to a different number for iterating through different amounts
	for _ in range(5):
		#print "Length of statuses", len(statuses)
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e: # No more results when next_results doesn't exist
			break

	# Create a dictionary from next_results, which has the following form:
		kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

		search_results = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']

	status_texts = [ status['text']
						for status in statuses ]

	screen_names = [ user_mention['screen_name']
						for status in statuses
							for user_mention in status['entities']['user_mentions'] ]

	hashtags = [ hashtag['text']
					for status in statuses
						for hashtag in status['entities']['hashtags'] ]

	# Compute a collection of all words from all tweets
	words = [ w
				for t in status_texts
						for w in t.split() ]

	# this is what we need to edit to change the data(get more or specify), I think changing all 5's to 50
	result = "Actual Tweets: "+json.dumps(status_texts[0:5], indent=1)+"\n"+"UsersNames that tweeted "+q+" :"+json.dumps(screen_names[0:5], indent=1)+"\n"+"HashTags used in those tweets"+json.dumps(hashtags[0:5], indent=1)
	print result
	'''
	ptt = PrettyTable(field_names=['UserName', 'HashTag', 'Tweet Text'])
	[ptt.add_row(row) for row in sorted(words, screen_names, reverse=True)[:5]]
	ptt.max_width['Tweet Text'] = 50
	ptt.align = '1'
	print ptt
	'''
	return result


#Performs a sentiment analysis on one word
def singleSentimentAnalysis(term):
	count = 1000
	#sentiment score for word 1

	search_results = twitter_api.search.tweets(q=term, count=count)

	statuses = search_results['statuses']

	# Iterate through 5 more batches of results by following the cursor

	for _ in range(5):
		#print "Length of statuses", len(statuses)
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e: # No more results when next_results doesn't exist
			break

	kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

	search_results = twitter_api.search.tweets(**kwargs)
	statuses += search_results['statuses']

	status_texts = [ status['text']
						for status in statuses ]

	screen_names = [ user_mention['screen_name']
						for status in statuses
							for user_mention in status['entities']['user_mentions'] ]

	hashtags = [ hashtag['text']
					for status in statuses
						for hashtag in status['entities']['hashtags'] ]

	# Compute a collection of all words from all tweets
	words = [ w
				for t in status_texts
					for w in t.split() ]

	sent_file = open('AFINN-111.txt')

	scores = {} # initialize an empty dictionary
	for line in sent_file:
		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		scores[term] = int(score)  # Convert the score to an integer.

	score = 0
	for word in words:
		uword = word.encode('utf-8')
		if uword in scores.keys():
			score = score + scores[word]

	return float(score)

# A function for computing lexical diversity
def lexical_diversity(tokens):
	return 1.0*len(set(tokens))/len(tokens)

# A function for computing the average number of words per tweet
def average_words(statuses):
	total_words = sum([ len(s.split()) for s in statuses ])
	return 1.0*total_words/len(statuses)

#Finds the most popular retweets
def popularRetweets():
	from urllib import unquote

	search_results = twitter_api.search.tweets(q='Chapman University', count=1000,result_type='recent') # adding result_type='recent' for recent tweets

	statuses = search_results['statuses']

	# Iterate through 5 more batches of results by following the cursor
	#try changing 5 to a different number for iterating through different amounts
	for _ in range(50):
		#print "Length of statuses", len(statuses)
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e: # No more results when next_results doesn't exist
			break

	# Create a dictionary from next_results, which has the following form:
		kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

		search_results = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']
	
	#tuple of these three values
	retweets = [
		(status['retweet_count'],
		 status['retweeted_status']['user']['screen_name'],
		 status['text'])
		for status in statuses
			if status.has_key('retweeted_status')
		]
	
	pt = PrettyTable(field_names=['Count' , 'Screen Name' , 'Text'])
	[ pt.add_row(row) for row in sorted(retweets, reverse=True)[:5] ]
	pt.max_width['Text'] = 50
	pt.align = 'l'
	print pt
	return str(pt)

#Displays popular trends
#right now we are only able to display us and world trends, since Chapman ID doesnt work
def popularTrends():
        #need to take name and tweet_volume variables and print them
        
        # The Yahoo! Where On Earth ID for the entire world is 1.
        # See https://dev.twitter.com/docs/api/1.1/get/trends/place and
        # http://developer.yahoo.com/geo/geoplanet/

        WORLD_WOE_ID = 1
        US_WOE_ID = 23424977
        CU_ID = 91656087


        world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
        us_trends = twitter_api.trends.place(_id=US_WOE_ID)
        #cu_trends = twitter_api.trends.place(_id=CU_ID)
        #this will compare world and us trends
        world_trends_set = set([trend['name']
                                for trend in world_trends[0]['trends']])

        world_trends_volume = set([trend['tweet_volume']
                                   for trend in world_trends[0]['trends']])

        us_trends_set = set([trend['name']
                             for trend in us_trends[0]['trends']])

        us_trends_volume = set([trend['tweet_volume']
                                for trend in us_trends[0]['trends']])

        common_trends = world_trends_set.intersection(us_trends_set)
        '''
        
        for world_trends_v in world_trends_volume

        
        '''
        print
        print
        print "Trends that are similar between the US and the World"
        print common_trends
        print
        print
        print "Volume of popular trends for the World"
        print world_trends_volume
        print "Volume of popular trends for the US"
        print us_trends_volume
        print
        #print "Test us trend = "+ us_trends_set[1]+ ". Number of "+us_trends_volume[1]
        
        
        #'''
        
        return '\n\nWorld trends with json.dumps\n\n'+str(json.dumps(world_trends, indent=1))+'\n\nUS trends with json.dumps\n\n'+str(json.dumps(us_trends, indent=1))+"\n\nTrends that are similar between the US and the World\n\n"+str(common_trends)+"\n\nVolume of trends\n\n"+str(world_trends_volume)+str(us_trends_volume)


def send_email(message):
	fromEmail = "herna181@mail.chapman.edu"
	toEmail = raw_input("Email to send to: ")
	subject = "ChapTweets Results"
	myString = "From: "+fromEmail+"\nTo: "+toEmail+"\nSubject: "+subject+"\n"+message

	server = smtplib.SMTP('smtp.chapman.edu', 25)
	server.sendmail(fromEmail, [toEmail], myString)
	server.quit()


#prints info to a csv file, need to error handel the csv file name and also work on certain info

def writeToCSV():
        csvFile = raw_input("Please enter a csv file name in the .csv format: ")
        q = raw_input('Enter a search term: ')
        result = printTwitterInfo(q)
        with open(csvFile, 'wb') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([result])
        return result




print "Welcome to ChapTweets!"
menu()

choice = raw_input("Please indicate which number option you would like to view or calculate: ")

print "Option #"+str(choice)
while(True):
	result = ""
	if choice == "1":
		result = printTwitterInfo("Chapman University")
	elif choice == "2":
		result = popularTrends()
	elif choice == "3":
		result = printTwitterInfo("#ChapmanU")
	elif choice == "4":
		result = printTwitterInfo("#CU")
	elif choice == "5":
		result = printTwitterInfo("#Fenestra")
	elif choice == "6":
		result = sentimentAnalysis("Chapman University", "University of Redlands")
	elif choice == "7":
		q1 = raw_input('Enter a search term: ')
		q2 = raw_input('Enter a search term: ')
		result = sentimentAnalysis(q1, q2)
	elif choice == "8":
		result = averageLength()
	elif choice == "9":
		result = averageHashtags()
	elif choice == "10":
		q = raw_input('Enter a search term: ')
		result = printTwitterInfo(q)
	elif choice == "11":
		word = raw_input("Please Enter a word to perform a sentient analysis: ")
		score = singleSentimentAnalysis(word)
		result = ("The Sentiment Analysis for " + str(word) + " is: " + str(score))
		print result
	elif choice == "12":
		result = writeToCSV()
	elif choice == "13":
		result = popularRetweets()
	elif choice == "14":
		print "Thank you!"
		break
	else:
		print "That was not an option, please try again"
		choice = raw_input("Please indicate which number option you would like to view or calculate: ")
		continue

	ifEmail = raw_input("Would you like to share these results? (y/n) ")
	if ifEmail == "y":
		send_email(result)
		print "Your message was sent."

	menu()
	choice = raw_input("Please indicate which number option you would like to view or calculate: ")
