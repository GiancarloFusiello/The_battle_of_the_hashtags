import factory
from django.contrib.auth.models import User

from battles.models import Battle, Hashtag


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    email = factory.Sequence(lambda n: 'user%d@example.com' % n)
    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'p@ssw0rd')

    is_superuser = False
    is_staff = True
    is_active = True


class HashtagFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Hashtag


class BattleFactory(factory.django.DjangoModelFactory):

    hashtag_1 = factory.SubFactory(HashtagFactory)
    hashtag_2 = factory.SubFactory(HashtagFactory)

    class Meta:
        model = Battle
        django_get_or_create = ('name',)
