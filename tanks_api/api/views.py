from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from .serializers import GameSerializer, PlayerSerializer, TargetSerializer
from .models import Game, Player, Target
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import json
import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# from rest_framework.decorators import api_view

# Create your views here.
firebase_url = "https://tanks-for-waiting.firebaseio.com"
put, delete = requests.put, requests.delete
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

class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def get_queryset(self):
        return self.queryset.filter(game_id=self.kwargs['games_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context().copy()
        context['game'] = get_object_or_404(Game, game_id=self.kwargs['games_pk'])
        return context

    def destroy(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        player = get_object_or_404(Player, player_id=body)
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            player = get_object_or_404(Player, player_id=body)
        except:
            return Response(status=403)
        game = get_object_or_404(Game, game_id=self.kwargs['games_pk'])
        target = self.get_object()
        current_location = requests.get(firebase_url + "/games/{}/tanks/{}.json".format(game.game_id, player.player_id)).json()
        if abs(current_location['x'] - target.x) < 100 and abs(current_location['y'] - target.y) < 100:
            player.add_point()
            delete(firebase_url + "/games/{}/targets/{}.json".format(game.game_id, target.target_id))
            self.perform_destroy(target)
            new_target = Target(game=game)
            new_target.save()
            game.save()
            return Response("Player")
        else:
            delete(firebase_url +"/games/{}/targets/{}.json".format(game.game_id, target.target_id))
            self.perform_destroy(target)
            new_target = Target(game=game)
            new_target.save()
            return Response("Else")


@receiver(post_save, sender=Game)
def put_tanks(sender, **kwargs):
    g = kwargs['instance']
    p = g.players.first()
    if len(g.players.all()) == 0:
        pass
    else:
        count = 1
        for p in g.players.all():
            put(firebase_url + '/games/{}/tanks/{}/x.json'.format(g.game_id, p.player_id), data=str(p.x * count))
            put(firebase_url + '/games/{}/tanks/{}/y.json'.format(g.game_id, p.player_id), data=str(p.y * count))
            put(firebase_url + '/games/{}/tanks/{}/score.json'.format(g.game_id, p.player_id), data=str(p.score))
            count += 2
        while len(g.targets.all()) < 5:
            t = Target(game=g)
            t.save()

@receiver(post_save, sender=Target)
def put_targets(sender, **kwargs):
    t = kwargs['instance']
    g = t.game
    if t.game != None:
        put(firebase_url + '/games/{}/targets/{}/x.json'.format(g.game_id, t.target_id), data=str(t.x))
        put(firebase_url + '/games/{}/targets/{}/y.json'.format(g.game_id, t.target_id), data=str(t.y))
        put(firebase_url + '/games/{}/targets/{}/is_hit.json'.format(g.game_id, t.target_id), data=str(0))
    else:
        pass
