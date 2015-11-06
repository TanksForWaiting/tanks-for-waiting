# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='target_id',
            field=models.UUIDField(unique=True, editable=False, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='player',
            name='player_id',
            field=models.UUIDField(unique=True, editable=False, default=uuid.uuid4),
        ),
    ]
