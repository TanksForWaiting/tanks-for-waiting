from rest_framework import serializers
from django.db.models import Count
from .models import Player, Game, Target
import requests

class TargetSerializer(serializers.ModelSerializer):
    x = serializers.IntegerField(read_only=True, min_value=0)
    y = serializers.IntegerField(read_only=True, min_value=0)
    game = serializers.StringRelatedField(read_only=True)
    target_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Target
        fields = ('x', 'y', 'game', 'target_id')

    def create(self, validated_data):
        t = Target(game=self.context['game'])
        t.save()
        return t



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

    def create(self, validated_data):
        # try:
        #     anno = Game.objects.annotate(num_players=Count('players'))
        #     over = anno.filter(num_players__gte=1)
        #     game = anno.filter(num_players__lte=3).order_by('-num_players')[0]
        #     game.players.add(self.context['player'])
        #     game.save()
        #     return game
        # except:
        g = Game()
        g.save()
        g.players.add(self.context['player'])
        g.save()
        return g
