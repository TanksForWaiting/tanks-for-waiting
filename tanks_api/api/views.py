from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from .serializers import GameSerializer, PlayerSerializer
from .models import Game, Player
# from rest_framework.decorators import api_view

# Create your views here.


class GameViewSet(viewsets.GenericViewSet,
                                CreateModelMixin,
                                ListModelMixin,
                                RetrieveModelMixin):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class PlayerViewSet(viewsets.GenericViewSet,
                                CreateModelMixin,
                                ListModelMixin,
                                RetrieveModelMixin):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
