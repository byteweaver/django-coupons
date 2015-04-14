# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='valid_until',
            field=models.DateTimeField(null=True, verbose_name='Valid until', blank=True),
            preserve_default=True,
        ),
    ]
