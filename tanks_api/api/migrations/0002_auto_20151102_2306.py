# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('player_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.RenameField(
            model_name='game',
            old_name='hash_id',
            new_name='game_id',
        ),
    ]
