# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0005_auto_20151105_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='redeemed_at',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='user',
        ),
    ]
