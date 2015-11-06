from django.db import models
import uuid
import random

# Create your models here.


class Game(models.Model):
    game_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def player_count(self):
        return self.players.count()

    def __str__(self):
        return str(self.game_id)


class Player(models.Model):
    player_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    score = models.PositiveSmallIntegerField(default=0)
    x = models.PositiveSmallIntegerField(default=24)
    y = models.PositiveSmallIntegerField(default=24)
    game = models.ForeignKey(Game, null=True, to_field='game_id', related_name='players')


    def __str__(self):
        return str(self.player_id)

class Target(models.Model):
    target_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    game = models.ForeignKey(Game, null=True, to_field='game_id', related_name='targets')
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    def save(self,*args, **kwargs):
        self.x = random.randint(20,480)
        self.y = random.randint(20,480)
        super(Target, self).save(*args, **kwargs)

    def __str__(self):
        return str((self.x, self.y))
