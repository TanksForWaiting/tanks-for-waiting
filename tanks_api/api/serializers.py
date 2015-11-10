from rest_framework import serializers
# from django.db.models import Count
from .models import Player, Game, Target
from django.db import transaction

class TargetSerializer(serializers.ModelSerializer):
    x = serializers.IntegerField(read_only=True, min_value=0)
    y = serializers.IntegerField(read_only=True, min_value=0)
    game = serializers.StringRelatedField(read_only=True)
    target_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Target
        fields = ('x', 'y', 'game', 'target_id')

    def create(self, validated_data):
        '''When you post to targets it makes a target in the game it pulls out
        of the url.'''
        target = Target.objects.create(game=self.context['game'])
        return target



class PlayerSerializer(serializers.ModelSerializer):
    player_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Player
        fields = ('player_id',)


class GameSerializer(serializers.ModelSerializer):
    game_id = serializers.UUIDField(read_only=True)
    players = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('game_id', 'players')

    @transaction.atomic
    def create(self, validated_data):
        '''Puts players into exisiting games before making new games.
        When you post a game with a payload of a player this looks at all
        the games in the database, finds those with between 1-3 players
        and puts the new player into a game with the fewest possible players.
        If it fails to find such a game it creates a new one for the player'''
        # try:
        #     add_player_count = Game.objects.annotate(num_players=Count('players'))
        #     over_one = add_player_count.filter(num_players__gte=1)
        #     game = over_one.filter(num_players__lte=3).order_by('num_players')[0]
        #     game.players.add(self.context['player'])
        #     game.save()
        #     return game
        # except:
        game = Game.objects.create()
        game.players.add(self.context['player'])
        game.save()
        self.context['player'].put()
        for _ in range(5 - len(game.targets.all())):
            Target.objects.create(game=game)
        return game
