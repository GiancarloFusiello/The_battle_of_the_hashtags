from rest_framework import serializers

from battles import models


def check_only_one_hashtag(hashtag):
    if hashtag and len(hashtag.split()) > 1:
        msg = 'Only one hashtag allowed per field'
        raise serializers.ValidationError(msg)


def check_hashtags_are_unique(hashtag_1, hashtag_2):
    if hashtag_1 == hashtag_2:
        msg = 'Hashtags are identical'
        raise serializers.ValidationError(msg)


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tweet
        fields = '__all__'


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hashtag
        fields = '__all__'


class BattleSerializer(serializers.ModelSerializer):

    status = serializers.CharField(allow_null=True, required=False)

    def validate(self, data):
        hashtag_1 = data.get('hashtag_1_name')
        check_only_one_hashtag(hashtag_1)

        hashtag_2 = data.get('hashtag_2_name')
        check_only_one_hashtag(hashtag_2)

        check_hashtags_are_unique(hashtag_1, hashtag_2)

        start = data.get('start')
        end = data.get('end')
        if start >= end:
            msg = 'Start date/time must be set before the end date/time'
            raise serializers.ValidationError(msg)

        return data

    class Meta:
        model = models.Battle
        fields = '__all__'
