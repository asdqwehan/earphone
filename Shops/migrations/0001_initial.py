# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_id', models.CharField(max_length=32)),
                ('goods_price', models.FloatField()),
                ('goods_now_price', models.FloatField()),
                ('goods_num', models.IntegerField()),
                ('goods_description', models.TextField()),
                ('goods_content', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('img_path', models.ImageField(upload_to='image')),
                ('img_label', models.CharField(max_length=32)),
                ('goods', models.ForeignKey(to='Shops.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('username', models.CharField(max_length=32)),
                ('mobilephone', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=32)),
                ('nickname', models.CharField(max_length=32)),
                ('photo', models.ImageField(upload_to='image')),
            ],
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=32)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='seller',
            field=models.ForeignKey(to='Shops.Seller'),
        ),
        migrations.AddField(
            model_name='goods',
            name='types',
            field=models.ForeignKey(to='Shops.Types'),
        ),
    ]
