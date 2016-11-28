import boto3
import json
from watson_developer_cloud import AlchemyLanguageV1
# from multiprocessing import Pool
from threading import Thread


class Worker(Thread):
	def __init__(self, message):
		Thread.__init__(self)
		self.message = message


	def run(self):
		try:
			message = self.message

			tweet = message

			response = alchemy_language.sentiment(text = tweet['text'])
			tweet['sentiment'] = response['docSentiment']['type']	

			print tweet

			publishResponse = client.publish(TopicArn = topicArn, Message = json.dumps(tweet))

		except:
			pass


class WorkerPool(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
    #Receive message (tweet) from kafka
        consumer = KafkaConsumer('tweet', group_id = 'tweet-stream', value_deserializer = lambda m: json.loads(m.decode('utf-8')))
		while True:
            for message in consumer:
				if message:
					worker = Worker(message)
					worker.start()


if __name__ == '__main__':

	# Get AWS SNS 
	client = boto3.client('sns')
	response = client.create_topic(Name = 'tweets2')
	topicArn = response['TopicArn']

	# Subscribe to SNS
	subscribeResponse = client.subscribe(TopicArn = topicArn, Protocol = 'http', Endpoint = 'Sample-env-1.89i8nxvymq.us-west-2.elasticbeanstalk.com')

	alchemy_language = AlchemyLanguageV1(api_key = '')

	pool = WorkerPool()
	pool.start()

