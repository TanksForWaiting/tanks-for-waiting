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
                ('game_id', models.UUIDField(unique=True, serialize=False, editable=False, primary_key=True, default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.UUIDField(unique=True, serialize=False, editable=False, primary_key=True, default=uuid.uuid4)),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('x', models.PositiveSmallIntegerField(default=24)),
                ('y', models.PositiveSmallIntegerField(default=24)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(to='api.Game', null=True, related_name='players')),
            ],
        ),
        migrations.CreateModel(
            name='RetiredPlayer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('target_id', models.UUIDField(unique=True, serialize=False, editable=False, primary_key=True, default=uuid.uuid4)),
                ('x', models.PositiveSmallIntegerField()),
                ('y', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(to='api.Game', null=True, related_name='targets')),
            ],
        ),
    ]
