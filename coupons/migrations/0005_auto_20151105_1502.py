# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_user_coupons(apps, schema_editor):
    Coupon = apps.get_model('coupons', 'Coupon')
    UserCoupon = apps.get_model('coupons', 'CouponUser')
    for coupon in Coupon.objects.all():
        if coupon.user is not None or coupon.redeemed_at is not None:
            UserCoupon.objects.create(
                coupon=coupon,
                user=coupon.user,
                redeemed_at=coupon.redeemed_at
            )


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0004_auto_20151105_1456'),
    ]

    operations = [
        migrations.RunPython(migrate_user_coupons),
    ]
