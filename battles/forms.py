from django import forms
from django.contrib import admin

from battles.models import Battle


def validate_only_one_hastag(hashtag):
    if hashtag and len(hashtag.split()) > 1:
        msg = 'Only one hashtag please'
        raise forms.ValidationError(msg)


def validate_hashtags_are_unique(hashtag_1, hashtag_2):
    if hashtag_1 == hashtag_2:
        msg = 'Hashtags are identical'
        raise forms.ValidationError(msg)


def validate_hashtags(data):
    hashtag_1 = data.get('hashtag_1_name', '')
    hashtag_2 = data.get('hashtag_2_name', '')
    validate_hashtags_are_unique(hashtag_1, hashtag_2)
    validate_only_one_hastag(hashtag_1)


class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = '__all__'

    def clean_hashtag_1_name(self):
        validate_hashtags(self.cleaned_data)
        return self.cleaned_data.get('hashtag_1_name', '')

    def clean_hashtag_2_name(self):
        validate_hashtags(self.cleaned_data)
        return self.cleaned_data.get('hashtag_2_name', '')

    def clean_start(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        if start and end and start >= end:
            msg = 'Start date/time must be set before the end date/time'
            raise forms.ValidationError(msg)
        return start

    def clean_end(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        if end and start and end <= start:
            msg = 'End date/time must be set after the start date/time'
            raise forms.ValidationError(msg)
        return end


class BattleAdmin(admin.ModelAdmin):
    form = BattleForm
