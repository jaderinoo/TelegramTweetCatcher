from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from telegram.ext import (Updater, CommandHandler)
import json 
import time
import datetime
import tweepy

#Fetch keys for bot and Coinmarketcap API
with open('keys.txt', 'r') as file:
    keys = file.read().split('\n')
     
currentDT = datetime.datetime.now()
cooldownSeconds = 0

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
        
    user = []
    ubikiri = api.get_user("Ubikiri_main")
    SN = api.get_user("SilentNotary")

    print("User details:")
    print(ubikiri.name + ", " + SN.name)
        
        
    return
 

def help(bot,update): 

    #Pull chat ID
    chat_id = update.message.chat_id
        
    #Initialize message
    message = "Please dont spam the bot, it only has 333 requests a day :) \nA 20 second cooldown is placed after each command execution. \n \n" + "Current command list: \n" + "/Price (coin symbol) \n" + "/Top \n" + "/Market \n"
    
    #Sends the help message to the user
    bot.sendMessage(chat_id, message)
        
    return
 
def cooldown(cooldownSeconds,currentDT):
    
    #Initialize the time in seconds needed to allow user input
    if cooldownSeconds == 0:
        cooldownSeconds = currentDT.second + 5
        print ("cc set to = " + str(currentDT.second))
        print ("Cooldown set to = " + str(cooldownSeconds))
       
    #Check if the initialized time is over 60, as the currentDT doesnt pass 60 
    if cooldownSeconds >= 60:
            cooldownSeconds = cooldownSeconds - 60
        
    #Continue to update currentDT until it matches the cooldown time
    while currentDT.second != cooldownSeconds:
        currentDT = datetime.datetime.now()
        time.sleep(1)
        print ("Current = " + str(currentDT.second))
        print ("Cooldown = " + str(cooldownSeconds))
 
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


