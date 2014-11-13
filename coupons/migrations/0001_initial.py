# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(help_text='Arbitrary coupon value', verbose_name='Value')),
                ('code', models.CharField(help_text='Leaving this field empty will generate a random code.', unique=True, max_length=30, verbose_name='Code', blank=True)),
                ('type', models.CharField(max_length=20, verbose_name='Type', choices=[(b'monetary', b'Money based coupon'), (b'percentage', b'Percentage discount'), (b'virtual_currency', b'Virtual currency')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('redeemed_at', models.DateTimeField(null=True, verbose_name='Redeemed at', blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='You may specify a user you want to restrict this coupon to.', null=True, verbose_name='User')),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
            bases=(models.Model,),
        ),
    ]
