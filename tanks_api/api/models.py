from django.db import models
import uuid

# Create your models here.


class Game(models.Model):
    game_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def player_count(self):
        return self.players.count()

    # def generate_id(self):
    #     '''Generates a unique 8 character game id'''
    #     import random
    #     import string
    #     unique_id = ''.join(random.SystemRandom().choice(
    #                 string.ascii_uppercase + string.digits) for _ in range(8))
    #     if Game.objects.filter(game_id=unique_id).count() > 0:
    #         return generate_id()
    #     else:
    #         self.game_id = unique_id
    #
    # def save(self, *args, **kwargs):
    #     '''Overwrites the save method to create a player id before saving'''
    #     if len(self.game_id) < 8:
    #         self.generate_id()
    #     super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.game_id)


class Player(models.Model):
    player_id = models.UUIDField(default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, null=True, to_field='game_id', related_name='players')

    # def generate_id(self):
    #     '''Generates a unique 8 character player id'''
    #     import random
    #     import string
    #     unique_id = ''.join(random.SystemRandom().choice(
    #                 string.ascii_uppercase + string.digits) for _ in range(8))
    #     if Player.objects.filter(player_id=unique_id).count() > 0:
    #         return generate_id()
    #     else:
    #         self.player_id = unique_id
    #
    # def save(self, *args, **kwargs):
    #     '''Overwrites the save method to create a player id before saving'''
    #     if len(self.player_id) < 8:
    #         self.generate_id()
    #     super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.player_id)
