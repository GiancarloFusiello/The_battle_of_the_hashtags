from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=180)
    screen_name = models.CharField(max_length=100)
    number_of_typos = models.IntegerField()
    tweeted_at = models.DateTimeField()


class Hashtag(models.Model):
    name = models.CharField(max_length=100)
    total_typos = models.IntegerField()
    tweet_with_most_typos = models.ForeignKey(Tweet)


class Battle(models.Model):
    name = models.CharField(max_length=100)
    hashtag_1_name = models.CharField(max_length=50)
    hashtag_2_name = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
