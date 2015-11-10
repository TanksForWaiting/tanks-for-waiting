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
                ('game_id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4, unique=True)),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('x', models.PositiveSmallIntegerField(default=24)),
                ('y', models.PositiveSmallIntegerField(default=24)),
                ('game', models.ForeignKey(related_name='players', to='api.Game', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('target_id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4, unique=True)),
                ('x', models.PositiveSmallIntegerField()),
                ('y', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(related_name='targets', to='api.Game', null=True)),
            ],
        ),
    ]
