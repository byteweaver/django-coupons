# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_coupon_valid_until'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Campaign',
                'verbose_name_plural': 'Campaigns',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='coupon',
            name='campaign',
            field=models.ForeignKey(related_name=b'coupons', verbose_name='Campaign', blank=True, to='coupons.Campaign', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_until',
            field=models.DateTimeField(help_text='Leave empty for coupons that never expire', null=True, verbose_name='Valid until', blank=True),
        ),
    ]
