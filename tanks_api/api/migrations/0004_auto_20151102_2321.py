# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_player_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='game',
            field=models.ForeignKey(related_name='players', to='api.Game', null=True),
        ),
    ]
