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

    def get_target_coordinates(self):
        targets_list = [(100, 20), (20,100), (250, 20), (20,250), (20, 400),(400,20),
                        (100, 480), (250,480), (400,480),(480,100), (480,250), (480,400),
                        (60,60),(440,440),(60,440),(440,60), (250,250),(200,225),(200,275),
                        (300, 225), (300,275), (250,400), (250,100)]
        for target in self.game.targets.all():
            targets_list.remove((target.x, target.y))
        if targets_list == []:
            targets_list = [(250, 250)]
        self.x, self.y = random.choice(targets_list)

    def save(self, *args, **kwargs):
        '''When you save a target it generates a random point between 20 and 480
        where it will spawn on both x and y axes.'''
        self.get_target_coordinates()
        super(Target, self).save(*args, **kwargs)

    def put(self):
        requests.put(firebase_url + "/games/{}/targets/{}.json".format(
            self.game.game_id, self.target_id), json={"x": self.x, "y": self.y, "is_hit": 0})

    def __str__(self):
        return str((self.x, self.y))
