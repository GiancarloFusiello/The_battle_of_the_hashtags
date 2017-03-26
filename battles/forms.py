from django import forms
from django.contrib import admin

from battles.models import Battle


def validate_hastag(hashtag):
    if hashtag and len(hashtag.split()) > 1:
        msg = 'This hashtag must be a single word'
        raise forms.ValidationError(msg)
    return hashtag


class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = '__all__'

    def clean_hashtag_1_name(self):
        hashtag = self.cleaned_data.get('hashtag_1_name', '')
        return validate_hastag(hashtag)

    def clean_hashtag_2_name(self):
        hashtag = self.cleaned_data.get('hashtag_2_name', '')
        return validate_hastag(hashtag)

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
