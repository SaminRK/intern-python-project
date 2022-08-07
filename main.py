from time import sleep

from pyjokes import get_joke

from api import create_user, get_tweets, post_tweet
from auth import auth_manager


def print_tweets_from_api(tweets: dict) -> None:

    for tweet in tweets:
        tweet_id = tweet["id"]
        tweet_athor_firstname = tweet["author"]["firstname"]
        created_at = tweet["created_at"]
        print(f"({tweet_id})  {tweet_athor_firstname} tweeted at {created_at}")
        print(tweet["text"])
        print()


def main():

    # response = create_user(username="SaminRK", firstname="Samin Rahman", lastname="Khan", password="password")

    print("Please log in to your account")

    username = input("username: ")
    password = input("password: ")

    print("Logging in...")

    auth_manager.set_username_password(username=username, password=password)
    auth_manager.get_auth_tokens()
    print("Logged in successfully")

    print("Checking recent tweets...")
    tweets = get_tweets()
    print_tweets_from_api(tweets)

    for i in range(10):
        tweets = get_tweets()
        tweet_text_set = set([tweet["text"] for tweet in tweets])

        joke = get_joke()
        while joke in tweet_text_set:
            joke = get_joke()
        print("Posting tweet")
        print(joke)
        post_tweet(text=joke)
        tweet_text_set.add(joke)

        print("Posted tweet. Sleeping for 1 min now.")
        sleep(60)


if __name__ == "__main__":
    main()
