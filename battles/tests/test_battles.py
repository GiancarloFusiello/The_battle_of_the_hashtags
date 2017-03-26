import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from battles.tests.factories import UserFactory, BattleFactory


class BattleTests(APITestCase):

    def setUp(self):
        user = UserFactory(username='lisa', password='l!s@')

        date = datetime.date(2017, 3, 1)
        time = datetime.time(14, 0, 0, tzinfo=timezone.get_current_timezone())
        start = datetime.datetime.combine(date, time)

        time = datetime.time(15, 0, 0, tzinfo=timezone.get_current_timezone())
        end = datetime.datetime.combine(date, time)

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

