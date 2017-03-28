from rest_framework import serializers

from battles import models
from battles.models import Hashtag, Battle


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

    total_typos = serializers.ReadOnlyField()

    class Meta:
        model = models.Hashtag
        exclude = ('id', 'tweet_with_most_typos',)

    def validate(self, data):
        check_only_one_hashtag(data.get('name'))
        return data


class BattleSerializer(serializers.ModelSerializer):

    hashtag_1 = HashtagSerializer()
    hashtag_2 = HashtagSerializer()
    status = serializers.CharField(allow_null=True, required=False)
    winning = serializers.CharField(allow_null=True, required=False)

    def validate(self, data):
        hashtag_1 = data.get('hashtag_1')
        hashtag_2 = data.get('hashtag_2')
        check_hashtags_are_unique(hashtag_1, hashtag_2)

        start = data.get('start')
        end = data.get('end')
        if start >= end:
            msg = 'Start date/time must be set before the end date/time'
            raise serializers.ValidationError(msg)

        return data

    def create(self, validated_data):
        hashtag_1, created = Hashtag.objects.get_or_create(
            name=validated_data['hashtag_1']['name']
        )
        hashtag_2, created = Hashtag.objects.get_or_create(
            name=validated_data['hashtag_2']['name']
        )
        battle = Battle.objects.create(name=validated_data['name'],
                                       hashtag_1=hashtag_1,
                                       hashtag_2=hashtag_2,
                                       start=validated_data['start'],
                                       end=validated_data['end'])
        return battle

    class Meta:
        model = models.Battle
        fields = '__all__'
