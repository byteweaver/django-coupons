# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupons', '0003_auto_20150416_0617'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('redeemed_at', models.DateTimeField(blank=True, verbose_name='Redeemed at', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='coupon',
            name='user_limit',
            field=models.PositiveIntegerField(verbose_name='User limit', default=1),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='type',
            field=models.CharField(choices=[('monetary', 'Money based coupon'), ('percentage', 'Percentage discount'), ('virtual_currency', 'Virtual currency')], verbose_name='Type', max_length=20),
        ),
        migrations.AddField(
            model_name='couponuser',
            name='coupon',
            field=models.ForeignKey(related_name='users', to='coupons.Coupon'),
        ),
        migrations.AddField(
            model_name='couponuser',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, verbose_name='User'),
        ),
    ]
