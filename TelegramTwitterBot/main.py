from telegram.ext import (Updater, CommandHandler)
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import telegram
import json 
import tweepy
import datetime

#Fetch keys for bot and twitter API
with open('keys.txt', 'r') as file:
    keys = file.read().split('\n')
    
#Grab follower ID's from follow.txt
with open('follow.txt', 'r') as file:
    follower_list = file.read().split('\n')

class TwitterStreamer():

    def __init__(self):
        pass

    #initializes auth and stream vars
    def stream_tweets(self, follower_list, chat_id):

        #Sets up auth and stream using keys.txt
        listener = StdOutListener(chat_id)
        auth = tweepy.OAuthHandler(keys[0], keys[1])
        auth.set_access_token(keys[2], keys[3])
        stream = Stream(auth, listener)
        
        #filters the stream to only recieve tweets from follow.txt items
        stream.filter(follow=follower_list)

class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            #Saves as a json
            d = json.loads(data)
            reply = d['in_reply_to_screen_name']    
            #Checks if the post is a reply       
            if(str(reply) == 'None'):
                #Checks if item is a retweet
                if('RT @' not in d['text']):
                    #If a new tweet is found, spit it out in the telegram channel
                    printData = d['id']
                    follower = d['user']['name']
                    bot = telegram.Bot(token=keys[4])
                    text = "New tweet from: " + follower + "\nhttps://twitter.com/" + follower + "/status/" + str(printData)
                    #Sends to channel/user
                    bot.sendMessage(keys[5], text)
                    #Print locally for console
                    print(text)
                    return True
            else:
                print("reply detected, not posted")
        except BaseException as e:
            print("Retweet detected, not posted")
        return True
          
    def on_error(self, status):
        print(status)

def start(bot,update):
    
    #Save channel name
    telegram_name = update.message.chat.title
    chat_id = update.message.chat_id
    
    #Pull chat ID
    keys[5] = str(chat_id)
    
    #Prints console information
    print("Container: " + telegram_name)
    print("----------------------\nBot started at: ")
    print(datetime.datetime.now())
    
    #initializes twitter stream vars
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(follower_list, chat_id)


#Initializes the telegram bot and listens for a command
def main():
    #Pulls Telegram api key from keys.txt and creates an updater
    telgramKey = keys[4]
    updater = Updater(telgramKey)     
    dp = updater.dispatcher
    
    #Creating Handler
    dp.add_handler(CommandHandler('start',start))

    #Start polling
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()


