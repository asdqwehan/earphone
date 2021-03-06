# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=32)),
                ('username', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='BuyCar',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.CharField(max_length=32)),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_price', models.FloatField()),
                ('goods_picture', models.ImageField(upload_to='image')),
                ('goods_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('email', models.EmailField(null=True, max_length=254, blank=True)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='EmailValid',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=32)),
                ('email_address', models.EmailField(max_length=254)),
                ('times', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=32)),
                ('order_time', models.DateTimeField(auto_now=True)),
                ('order_statue', models.CharField(max_length=32)),
                ('total', models.FloatField()),
                ('order_address', models.ForeignKey(on_delete=True, to='Buyers.Address')),
                ('user', models.ForeignKey(on_delete=True, to='Buyers.Buyer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('good_id', models.IntegerField()),
                ('good_name', models.CharField(max_length=32)),
                ('good_price', models.FloatField()),
                ('good_num', models.IntegerField()),
                ('goods_picture', models.ImageField(upload_to='')),
                ('order', models.ForeignKey(on_delete=True, to='Buyers.Order')),
            ],
        ),
        migrations.AddField(
            model_name='buycar',
            name='user',
            field=models.ForeignKey(on_delete=True, to='Buyers.Buyer'),
        ),
        migrations.AddField(
            model_name='address',
            name='buyer',
            field=models.ForeignKey(to='Buyers.Buyer'),
        ),
    ]
