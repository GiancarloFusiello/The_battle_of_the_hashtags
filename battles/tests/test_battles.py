import copy
import datetime
from unittest import skip

from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from battles.models import Hashtag
from battles.tests.factories import UserFactory, BattleFactory, HashtagFactory


class BattleTests(APITestCase):

    def setUp(self):
        user = UserFactory(username='lisa', password='l!s@')

        date = datetime.date(2017, 3, 1)
        time = datetime.time(14, 0, 0, tzinfo=timezone.get_current_timezone())
        start = datetime.datetime.combine(date, time)

        time = datetime.time(15, 0, 0, tzinfo=timezone.get_current_timezone())
        end = datetime.datetime.combine(date, time)

        london_hashtag = HashtagFactory(name='london')
        cambridge_hashtag = HashtagFactory(name='cambridge')

        self.battle_1 = BattleFactory(name='test battle 1',
                                      hashtag_1=london_hashtag,
                                      hashtag_2=cambridge_hashtag,
                                      start=start, end=end)

        self.battle_2 = BattleFactory(name='test battle 2',
                                      hashtag_1=london_hashtag,
                                      hashtag_2=cambridge_hashtag,
                                      start=start, end=end)

        self.user = user
        self.client.login(username='lisa', password='l!s@')

    def test_battles_can_be_retrieved(self):
        url = reverse('battle-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_a_single_battle_can_be_retrieved(self):
        url = reverse('battle-detail', args=[self.battle_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.battle_1.id)

    @skip('re-enable when battles can be created by post request')
    def test_a_battle_can_be_created(self):
        url = reverse('battle-list')
        payload = {'name': 'test battle',
                   'hashtag_1': 'london',
                   'hashtag_2': 'cambridge',
                   'start': '2017-03-01 13:00:00',
                   'end': '2017-03-01 14:00:00'}

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_response = copy.deepcopy(payload)
        expected_response['id'] = response.data.get('id')
        expected_response['status'] = 'battle is over'
        self.assertDictEqual(response.data, expected_response)

    @skip('re-enable when battles can be created by post request')
    def test_a_battle_cant_be_created_with_identical_hashtags(self):
        url = reverse('battle-list')
        payload = {'name': 'test battle',
                   'hashtag_1': 'london',
                   'hashtag_2': 'london',
                   'start': '2017-03-01 13:00:00',
                   'end': '2017-03-01 14:00:00'}

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'Hashtags are identical')

    @skip('re-enable when battles can be created by post request')
    def test_a_battle_cant_be_created_when_more_than_one_hashtag_in_field(self):
        url = reverse('battle-list')
        payload = {'name': 'test battle',
                   'hashtag_1': 'london cambridge',
                   'hashtag_2': 'cambridge',
                   'start': '2017-03-01 13:00:00',
                   'end': '2017-03-01 14:00:00'}

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'Only one hashtag allowed per field')

        payload = {'name': 'test battle',
                   'hashtag_1': 'london',
                   'hashtag_2': 'cambridge london',
                   'start': '2017-03-01 13:00:00',
                   'end': '2017-03-01 14:00:00'}

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'Only one hashtag allowed per field')

    @skip('re-enable when battles can be created by post request')
    def test_a_battle_cant_be_created_with_start_after_end(self):
        url = reverse('battle-list')
        payload = {'name': 'test battle',
                   'hashtag_1': 'london',
                   'hashtag_2': 'cambridge',
                   'start': '2017-03-01 15:00:00',
                   'end': '2017-03-01 14:00:00'}

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'Start date/time must be set before the end date/time')

        payload = {'name': 'test battle',
                   'hashtag_1': 'london',
                   'hashtag_2': 'cambridge',
                   'start': '2017-03-01 13:00:00',
                   'end': '2017-02-01 14:00:00'}

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'Start date/time must be set before the end date/time')

    @skip('re-enable when battles can be created by post request')
    def test_hashtag_objects_are_created_when_battle_is_created(self):
        url = reverse('battle-list')
        payload = {'name': 'test battle',
                   'hashtag_1': 'london',
                   'hashtag_2': 'cambridge',
                   'start': '2017-03-01 13:00:00',
                   'end': '2017-03-01 14:00:00'}

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        hashtags = Hashtag.objects.all()
        self.assertEqual(len(hashtags), 2)
