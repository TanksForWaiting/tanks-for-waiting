from rest_framework import serializers
from .models import Player, Game

class PlayerSerializer(serializers.ModelSerializer):
    player_id = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = Player
        fields = ('player_id',)


class GameSerializer(serializers.ModelSerializer):
    game_id = serializers.CharField(max_length=10, read_only=True)
    players = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('game_id', 'players')

    def create(self, validated_data):
        g = Game()
        g.save()
        g.players.add(self.context['player'])
        return g
