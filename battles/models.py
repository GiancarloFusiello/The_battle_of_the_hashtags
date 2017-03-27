from django.utils import timezone
from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=180)
    screen_name = models.CharField(max_length=100)
    number_of_typos = models.IntegerField()
    tweeted_at = models.DateTimeField()

    def __str__(self):
        return '{}: Tweet Object'.format(self.id)

    def __repr__(self):
        return '<{}: Tweet Object>'.format(self.id)


class Hashtag(models.Model):
    name = models.CharField(max_length=30)
    total_typos = models.IntegerField(default=0)
    tweet_with_most_typos = models.ForeignKey(Tweet, null=True, blank=True)

    def clean(self):
        self.name = self.name.strip().replace('#', '')

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)

    def __repr__(self):
        return '<{}: {}>'.format(self.id, self.name)


class Battle(models.Model):
    name = models.CharField(max_length=100)
    hashtag_1 = models.ForeignKey(Hashtag, related_name='hashtag_1')
    hashtag_2 = models.ForeignKey(Hashtag, related_name='hashtag_2')
    start = models.DateTimeField()
    end = models.DateTimeField()

    @property
    def status(self):
        now = timezone.now()
        if self.end < now:
            return 'battle is over'
        elif self.start > now:
            return 'awaiting battle'
        else:
            return 'in progress'

    def __str__(self):
        return '{}: {} - #{} vs #{} - {}'.format(
            self.id, self.name, self.hashtag_1.name, self.hashtag_2.name,
            self.status)

    def __repr__(self):
        return '<{}: {}>'.format(self.id, self.name)
