import os
import re
from datetime import datetime

import enchant
import twitter

from battles.models import Hashtag, Tweet, Battle


def get_typos(text):
    prefixes = ('@', '#', 'http', 'RT',)
    invalid_chars = ['!', '"', '@', '.', ',', ':', ';', '£', '$', '&amp', '…']
    # convert text to list of words and remove single characters from list
    words = [w for w in re.split(r'-+|\s+|\'+', text) if len(w) > 1]
    # filter invalid words such as hashtags, retweets, screen names and urls
    words = [w for w in words if not w.startswith(prefixes)]
    # filter invalid characters from words
    filtered_words = []
    for w in words:
        for i in invalid_chars:
            w = w.replace(i, '')
        if len(w) > 1:
            filtered_words.append(w)
    # names are considered typos if not capitalised (if in the dictionary)
    words = [w[0].upper() + w[1:] for w in filtered_words if len(w) > 1]
    # words spelled incorrectly evaluate to False
    chkr = enchant.Dict("en_GB")
    return list(filter(lambda w: not chkr.check(w), words))


def get_tweets_from_twitter(hashtag, since, until):
    api = twitter.Api(consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
                      consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
                      access_token_key=os.getenv('TWITTER_TOKEN_KEY'),
                      access_token_secret=os.getenv('TWITTER_TOKEN_SECRET'))

    query = 'l=en&q=%23{}%20since%3A{}%20until%3A{}'.format(hashtag, since, until)
    return api.GetSearch(raw_query=query)


def get_hashtag_info(hashtag_id, since, until):
    hashtag = Hashtag.objects.get(id=hashtag_id)
    tweets_from_twitter = get_tweets_from_twitter(hashtag.name, since, until)

    result = {'number of typos': 0,
              'tweet': None,
              'typos': None,
              'total_typos': 0}

    for tweet in tweets_from_twitter:
        typos = get_typos(tweet.text)
        result['total_typos'] += len(typos)
        if len(typos) > result['number of typos']:
            result['number of typos'] = len(typos)
            result['tweet'] = tweet
            result['typos'] = typos

    if result['tweet']:
        hashtag.total_typos = result['total_typos']
        new_tweet = Tweet.objects.create(
            text=result['tweet'].text,
            screen_name=result['tweet'].user.screen_name,
            number_of_typos=len(result['typos']),
            tweeted_at=datetime.strptime(
                result['tweet'].created_at, '%a %b %d %H:%M:%S %z %Y'
            )
        )
        hashtag.tweet_with_most_typos = new_tweet
        hashtag.save()


def battle(battle_id):
    battle = Battle.objects.get(id=battle_id)
    start_date = datetime.strftime(battle.start.date(), '%Y-%m-%d')
    end_date = datetime.strftime(battle.end.date(), '%Y-%m-%d')

    get_hashtag_info(battle.hashtag_1.id, start_date, end_date)
    get_hashtag_info(battle.hashtag_2.id, start_date, end_date)
