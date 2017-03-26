from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from battles.tests.factories import UserFactory, BattleFactory

DATETIME_FORMAT = settings.REST_FRAMEWORK['DATETIME_FORMAT']


class BattleTests(APITestCase):

    def setUp(self):
        user = UserFactory(username='lisa', password='l!s@')

        start = datetime.strptime('2017-03-01 14:00:00', DATETIME_FORMAT)
        end = datetime.strptime('2017-03-01 15:00:00', DATETIME_FORMAT)

        self.battle_1 = BattleFactory(name='test battle 1',
                                      hashtag_1_name='london',
                                      hashtag_2_name='cambridge',
                                      start=start, end=end)

        self.battle_2 = BattleFactory(name='test battle 2',
                                      hashtag_1_name='london',
                                      hashtag_2_name='cambridge',
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

