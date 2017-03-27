from battles import models, serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class BattlesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BattleSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = models.Battle.objects.all()
