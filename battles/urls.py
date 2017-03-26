from django.conf.urls import url, include
from rest_framework import routers

from battles.views import BattlesViewSet

router = routers.DefaultRouter()

router.register(r'battles', viewset=BattlesViewSet, base_name='battle')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
]
