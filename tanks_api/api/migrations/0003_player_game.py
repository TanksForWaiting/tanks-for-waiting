# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151102_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ForeignKey(to='api.Game', null=True),
        ),
    ]
