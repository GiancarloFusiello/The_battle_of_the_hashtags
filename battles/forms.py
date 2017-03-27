from django import forms
from django.contrib import admin

from battles.models import Battle, Hashtag


def validate_only_one_hastag(hashtag):
    if hashtag and len(hashtag.split()) > 1:
        msg = 'Only one hashtag allowed'
        raise forms.ValidationError(msg)


def validate_hashtags_are_unique(hashtag_1, hashtag_2):
    if hashtag_1 == hashtag_2:
        msg = 'Hashtags are identical'
        raise forms.ValidationError(msg)


def validate_hashtags(data):
    hashtag_1 = data.get('hashtag_1', '')
    if not isinstance(hashtag_1, str):
        hashtag_1 = hashtag_1.name

    hashtag_2 = data.get('hashtag_2', '')
    if not isinstance(hashtag_2, str):
        hashtag_2 = hashtag_2.name

    validate_hashtags_are_unique(hashtag_1, hashtag_2)


class BattleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BattleForm, self).__init__(*args, **kwargs)
        if self.initial and self.instance:
            # when loading saved battle convert foreign key id to name
            self.initial['hashtag_1'] = self.instance.hashtag_1.name
            self.initial['hashtag_2'] = self.instance.hashtag_2.name

    hashtag_1 = forms.CharField(max_length=30, required=True)
    hashtag_2 = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Battle
        fields = ['name', 'hashtag_1', 'hashtag_2', 'start', 'end']

    def clean_hashtag_1(self):
        validate_hashtags(self.cleaned_data)
        validate_only_one_hastag(self.cleaned_data['hashtag_1'])
        hashtag, created = Hashtag.objects.get_or_create(
            name=self.cleaned_data['hashtag_1']
        )
        return hashtag

    def clean_hashtag_2(self):
        validate_hashtags(self.cleaned_data)
        validate_only_one_hastag(self.cleaned_data['hashtag_2'])
        hashtag, created = Hashtag.objects.get_or_create(
            name=self.cleaned_data['hashtag_2']
        )
        return hashtag

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
