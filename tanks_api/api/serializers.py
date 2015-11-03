from rest_framework import serializers
from .models import Player, Game

class GameSerializer(serializers.HyperlinkedModelSerializer):
    game_id = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = Game
        fields = ('game_id',)

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    player_id = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = Player
        fields = ('player_id',)
