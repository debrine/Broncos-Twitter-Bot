import requests
from xml.etree import ElementTree
import time
import tweepy


#twitter credentials
twitter_credentials = open("twitter credentials.txt", "r")
consumer_key = twitter_credentials.readline().strip()
consumer_secret = twitter_credentials.readline().strip()
access_token = twitter_credentials.readline().strip()
access_secret = twitter_credentials.readline().strip()

#login to twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitter_api = tweepy.API(auth)

#website which holds live data for NFL games
url = 'http://www.nfl.com/liveupdate/scorestrip/ss.xml'

#access the webpage
live_data = requests.get(url)

#use ElementTree to parse the XML document
root = ElementTree.fromstring(live_data.content)

#access proper subchild 
games = root[0]

#find the data for the broncos game 

for game in games.iter():
    if game.get('hnn')  == 'broncos':
        broncos_game = game
        broncos_h_v = 'h'
    elif game.get('vnn') == 'broncos':
        broncos_game = game
        broncos_h_v = 'v'




#assign constants
if broncos_h_v == 'h':
    broncos_score_code = 'hs'
    opponent_score_code = 'vs'
    opponent_name = broncos_game.get('vnn')

else:
    broncos_score_code = 'vs'
    opponent_score_code = 'hs'
    opponent_name = broncos_game.get('hnn')




broncos_score_prev = broncos_game.get(broncos_score_code)
opponent_score_prev = broncos_game.get(opponent_score_code)


time.sleep(60)
#every minute, refresh the webpage and check for score changes
#if there are changes, send out an update tweet
while True:
    live_data = requests.get(url)
    root = ElementTree.fromstring(live_data.content)
    games = root[0]

    for game in games.iter():
    
        if (game.get('hnn') or game.get('vnn')) == 'broncos':
            
            broncos_game = game
        
    broncos_score = broncos_game.get(broncos_score_code)
    opponent_score = broncos_game.get(opponent_score_code)

    #if there is a score change, create the tweet and update status
    if (broncos_score != broncos_score_prev):
        broncos_gain = broncos_score - broncos_score_prev
        broncos_score_prev = broncos_score
        if broncos_gain == 1:
            tweet_content = ("#Broncos score " + str(broncos_gain) + " point! Score update: "
            "broncos "+ str(broncos_score) + " - " + str(opponent_score) + " " + opponent_name + " #Broncos")
        else:
            tweet_content = ("#Broncos score " + str(broncos_gain) + " points! Score update: "
            "broncos "+ str(broncos_score) + " - " + str(opponent_score) + " " + opponent_name + " #Broncos")
        twitter_api.update_status(tweet_content)
        

    elif (opponent_score != opponent_score_prev):
        opponent_gain = opponent_score - opponent_score_prev
        opponent_score_prev = opponent_score
        if opponent_gain == 1:
            tweet_content = (opponent_name + " score " + str(opponent_gain) + " point :( Score update: "
            "broncos "+ str(broncos_score) + " - " + str(opponent_score) + " " + opponent_name + " #Broncos")
        else:
            tweet_content = (opponent_name + " score " + str(opponent_gain) + " points :( Score update: "
            "broncos "+ str(broncos_score) + " - " + str(opponent_score) + " " + opponent_name + " #Broncos")
        twitter_api.update_status(tweet_content)
    time.sleep(60)

            

    

    
