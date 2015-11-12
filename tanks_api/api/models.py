from django.db import models
import uuid
import random
import requests

# Create your models here.
firebase_url = "https://tanks-for-waiting.firebaseio.com"


class Game(models.Model):
    game_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def player_count(self):
        return self.players.count()

    def __str__(self):
        return str(self.game_id)


class Player(models.Model):
    player_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    score = models.PositiveSmallIntegerField(default=0)
    x = models.PositiveSmallIntegerField(default=24)
    y = models.PositiveSmallIntegerField(default=24)
    game = models.ForeignKey(Game, null=True, related_name='players')
    start_time = models.DateTimeField(auto_now_add=True)

    def put(self):
        requests.put(firebase_url + '/games/{}/tanks/{}.json'.format(self.game.game_id,
                                                                     self.player_id), json={"x": self.x, "y": self.y, "direction": "E"})
        requests.put(firebase_url + '/games/{}/scores/{}.json'.format(
            self.game.game_id, self.player_id), data=str(self.score))

    def add_point(self):
        '''When a player gets a point it is recorded locally as well as
        put to the firebase database.'''
        self.score += 1
        self.save()
        requests.put(firebase_url + '/games/{}/scores/{}.json'.format(
            self.game.game_id, self.player_id), data=str(self.score))

    def __str__(self):
        return str(self.player_id)


class Target(models.Model):
    target_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    game = models.ForeignKey(Game, null=True, related_name='targets')
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        '''When you save a target it generates a random point between 20 and 480
        where it will spawn on both x and y axes.'''
        self.x = random.randint(20, 480)
        self.y = random.randint(20, 480)
        super(Target, self).save(*args, **kwargs)

    def put(self):
        requests.put(firebase_url + "/games/{}/targets/{}.json".format(
            self.game.game_id, self.target_id), json={"x": self.x, "y": self.y, "is_hit": 0})

    def __str__(self):
        return str((self.x, self.y))

# class Referral(models.Model):
#     url = models.URLField()
#     count = models.PositiveIntegerField(default=1)
#
#     def add(self):
#         self.count += 1
#         self.save()

class RetiredPlayer(models.Model):
    playtime = models.DateTimeField()

    def __str__(self):
        "Player played for {} minutes and {} seconds".format(int(self.playtime.seconds/60),
                                                                self.playtime.seconds % 60)
