from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from telegram.ext import (Updater, CommandHandler)
import json 
import tweepy

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

    while(len(follow) >= i):
        
        #Setup vars using the txt follow file
        userInfo = api.get_user(follow[i])

        
        #Print the current follower
        print("Follower = " + follow[i])
        
        #Load User response into data
        temp = follow[i]
        status_list = api.user_timeline(str(temp))
        status = status_list[0]
        dataUser = json.dumps(status._json)
        print(dataUser)   
        bot.sendMessage(chat_id, dataUser)
        
        #Increment i to move to next
        i = i + 1
    
    
    return
 

def help(bot,update): 

    #Pull chat ID
    chat_id = update.message.chat_id
        
    #Initialize message
    message = "Please dont spam the bot, it only has 333 requests a day :) \nA 20 second cooldown is placed after each command execution. \n \n" + "Current command list: \n" + "/Price (coin symbol) \n" + "/Top \n" + "/Market \n"
    
    #Sends the help message to the user
    bot.sendMessage(chat_id, message)
        
    return
 
#Initializes the telegram bot and listens for a command
def main():
    telgramKey = keys[4]
    updater = Updater(telgramKey)     
    dp = updater.dispatcher
    
    #Creating Handler
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))

    #Start polling
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()



