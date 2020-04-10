import tweepy 

# Fill the X's with the credentials obtained by 
# following the above mentioned procedure. 
consumer_key = "8pjMl7dXJqw4330E66Y3eo3qk"
consumer_secret = "sv2nBuZUMD1piw4eBkYyi8I0Vk8htBCoNzUhzDVZv3ARfDs7tv"
access_key = "4811440513-RxSCsUw3DAJ3ss8sfuPqtsGr2S60WjetsYJyBVl"
access_secret = "JvpYa1GB3BZMLid09vc6KsBeeBS6kKD9CWnSELh8zzi3P"

# Function to extract tweets 
def get_tweets(username): 
    
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_key, access_secret) 

    # Calling api 
    api = tweepy.API(auth) 

    # 200 tweets to be extracted 
    number_of_tweets=200
    tweets = api.user_timeline(screen_name=username) 

    # Empty Array 
    tmp=[] 

    # create array of tweet information: username, 
    # tweet id, date/time, text 
    tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created 
    for j in tweets_for_csv: 

      # Appending tweets to the empty array tmp 
      tmp.append(j) 

    # Printing the tweets 
    print(len(tmp))
    print(tmp) 


# Driver code 
if __name__ == '__main__': 

  # Here goes the twitter handle for the user 
  # whose tweets are to be extracted. 
  get_tweets("realDonaldTrump") 
