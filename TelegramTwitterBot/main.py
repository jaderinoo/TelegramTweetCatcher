from telegram.ext import (Updater, CommandHandler)
import json 
import tweepy
import time
import datetime

#Fetch keys for bot and Coinmarketcap API
with open('keys.txt', 'r') as file:
    keys = file.read().split('\n')
    
with open('follow.txt', 'r') as file:
    follow = file.read().split('\n')

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
    
    #Attemps to connect to api and posts an OK if it does
    try:
        api.verify_credentials()
        print("Authentication OK")
        bot.sendMessage(chat_id, "Service started")
    
    except:
        print("Error during authentication")
        
    #Initialize vars
    i = 0
    x = 0
    archive = ["null"]
    
    #Initializes the first position of archive
    temp = follow[i]
    status_list = api.user_timeline(str(temp))
    status = status_list[0]
    dataUser = json.dumps(status._json['id']) 
    archive[0] = str(dataUser)
        
    while(len(follow) >= i):
        #Posts current time
        print("-------------")
        print(datetime.datetime.now())
            
        #Print the current follower
        print("Follower = " + follow[i])
        
        #Cooldown Timer / Checks every 60 seconds
        print("Countdown: 60sec")
        time.sleep(30)
        
        print("Countdown: 30sec")
        time.sleep(30)
        
        #Updates Chatid
        chat_id = update.message.chat_id
            
        #Load User response into tempData
        temp = follow[i]
        status_list = api.user_timeline(str(temp))
        status = status_list[0]
        tempData = json.dumps(status._json['id'])        
        print("Current Tweet ID: " + str(tempData))
        
        #Check if the newly pulled status exists in the current set
        if tempData not in archive :
            #Adds the new data into the archive
            archive.append(str(tempData))
              
            #Updates Chatid
            chat_id = update.message.chat_id
            
            #Pulls the id from the json
            printData = json.dumps(status._json['id']) 
            
            #Doesnt send the initial tweet saved into archive
            if(len(follow) != x):
                x = x + 1
            
            #Format the string and sends it to the telegram user   
            if(len(follow) == x):
                text = "New tweet from: " + follow[i] + "\n https://twitter.com/" + follow[i] + "/status/" + str(printData)
                bot.sendMessage(chat_id, text)
                
        #Increment i to move to next
        i = i + 1
            
        #Reset i if follows is maxed
        if(len(follow) == i):
            i = 0

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



