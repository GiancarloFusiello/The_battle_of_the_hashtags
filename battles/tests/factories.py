import factory
from django.contrib.auth.models import User

from battles.models import Battle


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


class BattleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Battle
        django_get_or_create = ('name',)
