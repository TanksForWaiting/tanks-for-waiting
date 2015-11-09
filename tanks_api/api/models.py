from django.db import models
import uuid
import random
import requests

# Create your models here.


class Game(models.Model):
    game_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def player_count(self):
        return self.players.count()

    def __str__(self):
        return str(self.game_id)


class Player(models.Model):
    player_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    score = models.PositiveSmallIntegerField(default=0)
    x = models.PositiveSmallIntegerField(default=24)
    y = models.PositiveSmallIntegerField(default=24)
    game = models.ForeignKey(Game, null=True, related_name='players')

    def add_point(self):
        '''When a player gets a point it is recorded locally as well as
        put to the firebase database.'''
        self.score += 1
        self.save()
        requests.put('https://tanks-for-waiting.firebaseio.com/games/{}/tanks/{}/score.json'.format(self.game.game_id, self.player_id), data=str(self.score))

    def __str__(self):
        return str(self.player_id)

class Target(models.Model):
    target_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    game = models.ForeignKey(Game, null=True, related_name='targets')
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    def save(self,*args, **kwargs):
        '''When you save a target it generates a random point between 20 and 480
        where it will spawn on both x and y axes.'''
        self.x = random.randint(20,480)
        self.y = random.randint(20,480)
        super(Target, self).save(*args, **kwargs)

    def __str__(self):
        return str((self.x, self.y))
