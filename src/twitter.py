import tweepy
import credentials
import twitterSettings
from twilio.rest import Client


def returnTweets(username):
    auth = tweepy.OAuthHandler(credentials.twitter["consumer_key"], credentials.twitter["consumer_secret"])
    auth.set_access_token(credentials.twitter["access_token"], credentials.twitter["access_token_secret"])
    api = tweepy.API(auth)

    # Will be sent as a text message
    toText = []

    for tweet in tweepy.Cursor(api.user_timeline, id=username).items():
        # Twitter's api doesn't provide a way to find tweets within a certain date range, so we'll use likes
        if not tweet.favorited:
            api.create_favorite(tweet.id)
            addToText = {}
            addToText["author"] = tweet.user.name
            addToText["message"] = tweet._json["text"]
            toText.append(addToText)
        else:
            # Once we hit the first tweet that has been liked, we can stop looping over the rest
            return toText


def sendTexts(tweetQueue):
    # Since I'm paying per text, I'm sending everything in one text.
    # It's less readable, but I don't want to spend much on a side project
    client = Client(credentials.twilio["accountSID"], credentials.twilio["authToken"])
    for number in credentials.twilio["cellPhone"]:
        client.messages.create(body=str(tweetQueue), from_=credentials.twilio["twilioNumber"], to=number)

if __name__ == "__main__":
    tweetQueue = []
    for user in twitterSettings.followNames:
        tweetQueue += returnTweets(user)
    if tweetQueue:
        sendTexts(tweetQueue)
