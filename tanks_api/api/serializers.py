from rest_framework import serializers
from .models import Player, Game, Target
import requests

class TargetSerializer(serializers.ModelSerializer):
    x = serializers.IntegerField(read_only=True, min_value=0)
    y = serializers.IntegerField(read_only=True, min_value=0)
    game = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Target
        fields = ('x', 'y', 'game')

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
        g = Game()
        g.save()
        g.players.add(self.context['player'])
        return g
