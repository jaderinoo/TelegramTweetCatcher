from tweepy import Stream
from tweepy import OAuthHandler
from telegram.ext import (Updater, CommandHandler)
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

analyzer = SentimentIntensityAnalyzer()

#Fetch keys for bot and Coinmarketcap API
with open('keys.txt', 'r') as file:
    keys = file.read().split('\n')
    
with open('follow.txt', 'r') as file:
    follow = file.read().split('\n')
    
conn = sqlite3.connect('twitter.db')
c = conn.cursor()

telgramKey = keys[4]
updater = Updater(telgramKey)
dp = updater.dispatcher

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
    conn.commit()
create_table()

#consumer key, consumer secret, access token, access secret.
ckey= keys[0]
csecret= keys[1]
atoken= keys[2]
asecret= keys[3]

class listener(StreamListener):

    def on_data(self, data, bot, update):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                  (time_ms, tweet, sentiment))
            conn.commit()
                   
            chat_id = update.message.chat_id
            bot.sendMessage(chat_id, temp)

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)
        

while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        
        #Sort through follow and add to stream
        temp = follow[0]
        i = 1
        while(len(follow) >= i):
        
            #Print the current follower
            print(temp)
        
            #Load User response into data
            temp += ", " + str(follow[i]) 
        
            #Increment i to move to next
            i += 1
            
        

        #twitterStream.filter(follow=[follow])
        #twitterStream.filter(follow=[follow[1]])
        
    except Exception as e:
        print(str(e))
        time.sleep(5)
   
#Start polling
updater.start_polling()
updater.idle()   