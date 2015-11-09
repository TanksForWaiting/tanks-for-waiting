from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from .serializers import GameSerializer, PlayerSerializer, TargetSerializer
from .models import Game, Player, Target
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from rest_framework import status
from rest_framework.response import Response
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
        deserializing input, and for serializing output.  In this case we are
        getting the player_id out of the included payload so we can put them into
        a game.
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
        '''When you GET targets only shows targets for the game you care about'''
        return self.queryset.filter(game_id=self.kwargs['games_pk'])

    def get_serializer_context(self):
        '''Gets the game_id out of the url'''
        context = super().get_serializer_context().copy()
        context['game'] = get_object_or_404(Game, game_id=self.kwargs['games_pk'])
        return context

    def destroy(self, request, *args, **kwargs):
        '''Destroys the target both locally and in firebaseio
        Tries to find a player_id in the payload, if it doesn't it assumes
        that the target was hit by a non-player (spawned in a wall)
        If it finds a player and that player's location in firebase is near enough
        the target in the local database that player gets a point.'''
        try:
            player = get_object_or_404(Player, player_id=self.request.data['player_id'])
            game = get_object_or_404(Game, game_id=self.kwargs['games_pk'])
            target = self.get_object()
            r = requests.get("https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}.json".format(game.game_id, player.player_id))
            if abs(r.json()['x'] - target.x) < 30 and abs(r.json()['y'] - target.y) < 30:
                player.add_point()
                requests.delete("https://tanks-for-waiting.firebaseio.com/games/{}/targets/{}.json".format(game.game_id, target.target_id))
                self.perform_destroy(target)
                t = Target(game=game)
                t.save()
                return Response("Target Destroyed!")
            else:
                return Response("nope")
        except:
            game = get_object_or_404(Game, game_id=self.kwargs['games_pk'])
            target = self.get_object()
            requests.delete("https://tanks-for-waiting.firebaseio.com/games/{}/targets/{}.json".format(game.game_id, target.target_id))
            self.perform_destroy(target)
            t = Target(game=game)
            t.save()
            return Response("Target Destroyed By Non-Player")


@receiver(post_save, sender=Game)
def put_tanks(sender, **kwargs):
    '''After saving a game if it has players it creates the game in firebase.
    It ensures all of the targets in the game locally are in firebase and then
    creates more until there are 5.  It also puts each player into firebase.'''
    g = kwargs['instance']
    if len(g.players.all()) == 0:
        pass
    else:
        player = 1
        for p in g.players.all(): #Puts players into starting locations.
            if player == 1:
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/x.json'.format(g.game_id, p.player_id), data=str(20))
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/y.json'.format(g.game_id, p.player_id), data=str(20))
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/dir.json'.format(g.game_id, p.player_id), data=str(1))
            elif player == 2:
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/x.json'.format(g.game_id, p.player_id), data=str(480))
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/y.json'.format(g.game_id, p.player_id), data=str(480))
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/dir.json'.format(g.game_id, p.player_id), data=str(2))
            elif player == 3:
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/x.json'.format(g.game_id, p.player_id), data=str(480))
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/y.json'.format(g.game_id, p.player_id), data=str(20))
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/dir.json'.format(g.game_id, p.player_id), data=str(2))
            else:
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/x.json'.format(g.game_id, p.player_id), data=str(20))
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/y.json'.format(g.game_id, p.player_id), data=str(480))
                requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/dir.json'.format(g.game_id, p.player_id), data=str(1))
            requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/scores/{}/score.json'.format(g.game_id, p.player_id), data=str(p.score))
            player += 1
        for t in g.targets.all():
            requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/targets/{}/x.json'.format(g.game_id, t.target_id), data=str(t.x))
            requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/targets/{}/y.json'.format(g.game_id, t.target_id), data=str(t.y))
        while len(g.targets.all()) < 5:
            t = Target(game=g)
            t.save()


@receiver(post_save, sender=Target)
def put_targets(sender, **kwargs):
    '''Whever a target is saved locally if it has a game assigned it is put
    into firebase'''
    t = kwargs['instance']
    g = t.game
    if t.game != None:
        requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/targets/{}/x.json'.format(g.game_id, t.target_id), data=str(t.x))
        requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/targets/{}/y.json'.format(g.game_id, t.target_id), data=str(t.y))
    else:
        pass
