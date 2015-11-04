from django.db import models
import uuid

# Create your models here.


class Game(models.Model):
    game_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def player_count(self):
        return self.players.count()

    def __str__(self):
        return str(self.game_id)


class Player(models.Model):
    player_id = models.UUIDField(default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, null=True, to_field='game_id', related_name='players')


    def __str__(self):
        return str(self.player_id)
