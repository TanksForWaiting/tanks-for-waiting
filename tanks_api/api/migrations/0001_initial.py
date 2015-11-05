# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('game_id', models.UUIDField(editable=False, default=uuid.uuid4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('player_id', models.UUIDField(editable=False, default=uuid.uuid4)),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('x', models.PositiveSmallIntegerField(default=24)),
                ('y', models.PositiveSmallIntegerField(default=24)),
                ('game', models.ForeignKey(null=True, related_name='players', to_field='game_id', to='api.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('x', models.PositiveSmallIntegerField()),
                ('y', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(null=True, related_name='targets', to_field='game_id', to='api.Game')),
            ],
        ),
    ]
