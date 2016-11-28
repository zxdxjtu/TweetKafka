# Important the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 
#from elasticsearch import Elasticsearch
import requests
import json
import boto3




access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


# This is a basic listener that just prints received tweets to stdout
class StdOutListener(StreamListener):

	def on_error(self, status):
		#print status
		pass


	def on_status(self, status):
		try:
			if status.coordinates:
				#print status
				tweet = {}
				tweet['user'] = status.user.screen_name
				tweet['text'] = status.text
				tweet['location'] = status.coordinates['coordinates']
				tweet['time'] = str(status.created_at)
                #kafka send to consumer
				response = producer.send('tweet', value = tweet)


				print tweet
		except Exception as e:
			print 'Error! {0}: {1}'.format(type(e), str(e))

if __name__ == '__main__':

	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
        #Producer
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))


	stream.filter(track = ['job','game','love','food','fashion','NewYork','LOL','Trump','Hilary','hello'])
