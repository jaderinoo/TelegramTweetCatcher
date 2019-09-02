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
        print("Authentication OK \nService Started! \nPlease enter a name for this container:")
        containerName = input()
        
    except:
        print("Error during authentication")
        
    #Initialize vars
    i = 0
    x = 0
    archive = ["null"]
    
    #Initializes the first position of archive and posts initial logs
    temp = follow[i]
    status_list = api.user_timeline(str(temp))
    status = status_list[0]
    dataUser = json.dumps(status._json['id']) 
    archive[0] = str(dataUser)
      
    #Posts current time
    print("-------------")
    print("Container: " + containerName)
    print(datetime.datetime.now())
                
    #Cooldown Timer / Checks every 60 seconds
    print("Countdown: 90sec")
    time.sleep(45)
        
    print("Countdown: 90sec")
    time.sleep(45)
    
    print("-------------")
    
    try:
        while(len(follow) >= i):
            
            #Wait 1 second before pulling next tweet
            time.sleep(1) 
                     
            #Print the current follower
            print("Follower = " + follow[i])
    
            
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
                #Posts current time
                print("-------------")
                print("Container: " + containerName)
                print(datetime.datetime.now())
                            
                #Cooldown Timer / Checks every 60 seconds
                print("Countdown: 90sec")
                time.sleep(45)
                    
                print("Countdown: 90sec")
                time.sleep(45)
                
                print("-------------")
                
                #Reset i to 0 and loop back
                i = 0
                
    except:
        print("Error: Unknown \nBot Stopped!")       
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



