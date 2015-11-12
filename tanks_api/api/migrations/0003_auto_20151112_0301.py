# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_referral'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetiredPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('playtime', models.DurationField()),
            ],
        ),
        migrations.DeleteModel(
            name='Referral',
        ),
        migrations.AddField(
            model_name='player',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 12, 3, 1, 45, 376617, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
