# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0006_auto_20151105_1509'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='couponuser',
            unique_together=set([('coupon', 'user')]),
        ),
    ]
