from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from .serializers import GameSerializer, PlayerSerializer, TargetSerializer
from .models import Game, Player, Target, Referral
# from django.db.models.signals import post_save
# from django.dispatch import receiver
import requests
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.decorators import api_view

# Create your views here.
firebase_url = "https://tanks-for-waiting.firebaseio.com"
get, put, delete = requests.get, requests.put, requests.delete

def redirect_to_game(request):
    return redirect("https://tanks-for-waiting.firebaseapp.com/")



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


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def create(self, request, *args, **kwargs):
        try:
            try:
                referral = get_object_or_404(Referral, url=request.META.HTTP_REFERER)
                referral.add()
            except status.HTTP_404_NOT_FOUND:
                Referral.objects.create(site=request.META.HTTP_REFERER)
        except:
            pass
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        '''Destroys the target both locally and in firebaseio
        Tries to find a player_id in the payload, if it doesn't it returns a 403 error.
        If it finds a player and that player's location in firebase is near enough
        the target in the local database that player gets a point.  If the player is not
        close enough the target is still destroyed but the player doesn't get a point.'''
        try:
            body = str(request.body.decode('utf-8'))
            player = get_object_or_404(Player, player_id=body)
        except:
            return Response(status=403)
        target = self.get_object()
        game = target.game
        current_location = get(firebase_url + "/games/{}/tanks/{}.json".format(game.game_id, player.player_id)).json()
        target_id = target.target_id
        if abs(current_location['x'] - target.x) < 100 and abs(current_location['y'] - target.y) < 100:
            player.add_point()
            self.perform_destroy(target)
            delete(firebase_url + "/games/{}/targets/{}.json".format(game.game_id, target_id))
            new_target = Target.objects.create(game=game)
            new_target.put()
            return Response("Player")
        else:
            self.perform_destroy(target)
            delete(firebase_url +"/games/{}/targets/{}.json".format(game.game_id, target_id))
            new_target = Target.objects.create(game=game)
            new_target.put()
            return Response("Else")


# @receiver(post_save, sender=Game)
# def put_tanks(sender, **kwargs):
#     '''After saving a game if it has players it creates the game in firebase.
#     It ensures all of the targets in the game locally are in firebase and then
#     creates more until there are 5.  It also puts each player into firebase.'''
#     game = kwargs['instance']
#     if len(game.players.all()) == 0:
#         pass
    # else:
    #     current_player = 1
        # for player in game.players.all(): #Puts players into starting locations.
        #     # if current_player == 1:
        #     # player.put(game_id, player_id, x=1, y=1, direction="E")
        #     put(firebase_url + '/games/{}/tanks/{}.json'.format(game.game_id, player.player_id), json={"x":20,"y":20,"direction":"E"})
        #     # elif current_player == 2:
        #     #     put(firebase_url + '/games/{}/tanks/{}.json'.format(game.game_id, player.player_id), json={"x":480,"y":480,"direction":"W"})
        #     # elif current_player == 3:
        #     #     put(firebase_url + '/games/{}/tanks/{}.json'.format(game.game_id, player.player_id), json={"x":480,"y":20,"direction":"W"})
        #     # else:
        #     #     put(firebase_url + '/games/{}/tanks/{}.json'.format(game.game_id, player.player_id), json={"x":20,"y":480,"direction":"E"})
        #     put(firebase_url + '/games/{}/scores/{}.json'.format(game.game_id, player.player_id), data=str(player.score))
        #     current_player += 1
    # else:
    #     for target in game.targets.all():
    #         target.put()
        # while len(game.targets.all()) < 5:
        #     new_target = Target(game=game)
        #     new_target.save()


# @receiver(post_save, sender=Target)
# def put_targets(sender, **kwargs):
#     '''Whever a target is saved locally if it has a game assigned it is put
#     into firebase'''
#     new_target = kwargs['instance']
#     if new_target.game != None:
#         new_target.put()
#     else:
#         pass
