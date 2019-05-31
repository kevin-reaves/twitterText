import tweepy
import credentials
import twitterSettings

def returnTweets(username):
    auth = tweepy.OAuthHandler(credentials.twitter["consumer_key"], credentials.twitter["consumer_secret"])
    auth.set_access_token(credentials.twitter["access_token"], credentials.twitter["access_token_secret"])
    api = tweepy.API(auth)

    toText = []

    for tweet in tweepy.Cursor(api.user_timeline, id=username).items():
        if not tweet.favorited:
            api.create_favorite(tweet.id)
            addToText = {}
            addToText["author"] = tweet.user.name
            addToText["message"] = tweet._json["text"]
            toText.append(addToText)
        else:
            # Once we hit the first tweet that has been liked, we can stop looping over the rest
            return toText



if __name__ == "__main__":
    tweetQueue = []
    for user in twitterSettings.followNames:
        tweetQueue += returnTweets(user)
