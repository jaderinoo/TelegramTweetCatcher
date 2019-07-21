from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from telegram.ext import (Updater, CommandHandler)
import json 
import tweepy
import time

#Fetch keys for bot and Coinmarketcap API
with open('keys.txt', 'r') as file:
    keys = file.read().split('\n')
    
with open('follow.txt', 'r') as file:
    follow = file.read().split('\n')

class followlst(object):
    def __init__(self, name=None):
        self.name = name

def start(bot,update):
    
    #Testing keys 
    print(keys[0] + "," + keys[1]+ "," + keys[2]+ "," + keys[3])
    
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])

    # Create API object
    api = tweepy.API(auth)
    
    #Pull chat ID
    chat_id = update.message.chat_id
    
    try:
        api.verify_credentials()
        print("Authentication OK")
        
        #Initialize message
        message = "Authentication OK"
        
        #Sends the help message to the user
        bot.sendMessage(chat_id, message)
    
    except:
        print("Error during authentication")
        
    
    i = 0
    x = 1
    archive = ["null"]
    
    while True:
        temp = follow[i]
        status_list = api.user_timeline(str(temp))
        status = status_list[0]
        dataUser = json.dumps(status._json) 
        archive[0] = str(dataUser)    
        time.sleep(1)
        while(len(follow) >= i):
            #Setup vars using the txt follow file
            chat_id = update.message.chat_id
    
            #Print the current follower
            print("Follower = " + follow[i])
            
            #Load User response into data
            temp = follow[i]
            status_list = api.user_timeline(str(temp))
            status = status_list[0]
            tempData = json.dumps(status._json)        
            
            if tempData not in archive :
                archive.append(str(tempData))
                print("!=")
                chat_id = update.message.chat_id
                
                
                
                #Format the string with data 
                string = "This is a string"
                bot.sendMessage(chat_id, string)
                
            
            #Increment i to move to next
            i = i + 1
            
            if(len(follow) == i):
                i = 0
        x += 1

#Initializes the telegram bot and listens for a command
def main():
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



