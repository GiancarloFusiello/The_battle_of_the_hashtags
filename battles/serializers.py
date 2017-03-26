from rest_framework import serializers

from battles import models


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tweet
        fields = '__all__'


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hashtag
        fields = '__all__'


class BattleSerializer(serializers.ModelSerializer):

    status = serializers.CharField()

    class Meta:
        model = models.Battle
        fields = '__all__'
