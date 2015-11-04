# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151103_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='player_id',
            field=models.CharField(unique=True, max_length=10),
        ),
    ]
