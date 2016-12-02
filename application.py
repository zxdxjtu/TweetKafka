from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import json
import requests

application = Flask(__name__)

socketio = SocketIO(application)

socketConnected = False


@application.route('/', methods=['GET', 'POST'])
def hello_world():
    global socketConnected
    #Receiving AWS SNS
    if request.method == 'POST':

        try:
            js = json.loads(request.data)
        except:
            pass

        print js
        hdr = request.headers.get('X-Amz-Sns-Message-Type')

        # Subscribe to the SNS topic
        if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
            r = requests.get(js['SubscribeURL'])

        if hdr == 'Notification':
            tweet = js['Message']
            print tweet
            postURL = 'ENDPOINT/tweetmap/tweet'
            r = requests.post(postURL, json = tweet)
            if socketConnected:
                socketio.emit('realTimeResponse', tweet)

    return render_template('TwitterMap.html')


@application.route('/search')
def handle_search():
    return render_template('searchPage.html')


@socketio.on('realTime')
def handle_realtime_event(message):
    global socketConnected
    socketConnected = True


    queryURL = 'ENDPOINT/tweetmap/_search?q=*:*&size=10000'
    response = requests.get(queryURL)
    results = json.loads(response.text)

    tweets = []
    for result in results['hits']['hits']:
        tweet = {'sentiment': result['_source']['sentiment'], 'longitude': result['_source']['longitude'],
                 'latitude': result['_source']['latitude']}
        tweets.append(tweet)

    send(json.dumps(tweets))

#Search tweets from elastic search to display on the front end
@socketio.on('message')
def handle_message(message):
    if message == 'Init':
        queryURL = 'ENDPOINT/tweetmap/_search?q=*:*&size=10000'
        response = requests.get(queryURL)
        results = json.loads(response.text)

    else:

        queryKeyWord = message.replace(' ', '%20')
        queryURL = 'ENDPOINT/tweetmap/_search?q=' + queryKeyWord + '&size=10000'
        response = requests.get(queryURL)
        results = json.loads(response.text)

    tweets = []
    for result in results['hits']['hits']:
        
        tweets.append({'sentiment': result['_source']['sentiment'], 'longitude': result['_source']['longitude'],
                      'latitude': result['_source']['latitude']})

    send(json.dumps(tweets))


if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0' debug=True)
