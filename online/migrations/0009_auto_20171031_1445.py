# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-31 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0008_auto_20171031_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='table_Initiation',
            fields=[
                ('立项识别码', models.AutoField(primary_key=True, serialize=False)),
                ('项目名称', models.CharField(max_length=255, unique=True)),
                ('分项名称', models.CharField(max_length=255, null=True, unique=True)),
                ('父项立项识别码', models.IntegerField(max_length=255, null=True)),
                ('建设单位识别码', models.IntegerField(max_length=255, null=True)),
                ('代建单位识别码', models.IntegerField(max_length=255, null=True)),
                ('立项文件名称', models.CharField(max_length=255, null=True)),
                ('立项时间', models.DateField()),
                ('项目概算', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('立项备注', models.TextField(null=True)),
            ],
            options={
                'ordering': ['立项识别码'],
                'verbose_name': '立项信息表',
                'db_table': 'TABEL_立项信息',
            },
        ),
        migrations.AlterUniqueTogether(
            name='table_initiation',
            unique_together=set([('项目名称', '分项名称')]),
        ),
    ]
