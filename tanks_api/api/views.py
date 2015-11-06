from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from .serializers import GameSerializer, PlayerSerializer
from .models import Game, Player
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
# from rest_framework.decorators import api_view

# Create your views here.


class GameViewSet(viewsets.GenericViewSet,
                                CreateModelMixin,
                                ListModelMixin,
                                RetrieveModelMixin):

    queryset = Game.objects.all()
    serializer_class = GameSerializer


    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        try:
            player_id = kwargs['data']['player_id']
            serializer_class = self.get_serializer_class()
            kwargs['context'] = {'player':get_object_or_404(Player, player_id=player_id)}
            return serializer_class(*args, **kwargs)
        except KeyError:
            serializer_class = self.get_serializer_class()
            kwargs['context'] = self.get_serializer_context()
            return serializer_class(*args, **kwargs)


class PlayerViewSet(viewsets.GenericViewSet,
                                CreateModelMixin,
                                ListModelMixin,
                                RetrieveModelMixin):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

# @receiver(post_save, sender=Game)
# def hello_world(sender, **kwargs):
#     # return print(kwargs['instance'])
#     g = kwargs['instance']
#     p = g.players.first()
#     if len(g.players.all()) == 0:
#         pass
#     else:
#         return print('{}       {}'.format(g.game_id, p.player_id))
#     # try requests.put('https://tanks-for-waiting.firebaseapp.com/games/{}/tanks/{}'.format(g.game_id, p.player_id), data={"x":20,"y":20})
