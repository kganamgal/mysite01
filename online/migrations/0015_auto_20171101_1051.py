# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-01 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0014_table_contract'),
    ]

    operations = [
        migrations.CreateModel(
            name='table_Alteration',
            fields=[
                ('变更识别码', models.BigAutoField(primary_key=True, serialize=False)),
                ('立项识别码', models.BigIntegerField(null=True)),
                ('合同识别码', models.BigIntegerField(null=True)),
                ('变更类型', models.CharField(max_length=255, null=True, unique=True)),
                ('变更编号', models.CharField(max_length=255, null=True, unique=True)),
                ('变更主题', models.CharField(max_length=255, null=True, unique=True)),
                ('变更登记日期', models.DateField(null=True)),
                ('变更生效日期', models.DateField(null=True)),
                ('变更原因', models.TextField(null=True)),
                ('预估变更额度', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('变更额度', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('变更备注', models.TextField(null=True)),
            ],
            options={
                'ordering': ['变更识别码'],
                'verbose_name': '变更信息表',
                'db_table': 'TABEL_变更信息',
            },
        ),
        migrations.CreateModel(
            name='table_Budget',
            fields=[
                ('预算识别码', models.BigAutoField(primary_key=True, serialize=False)),
                ('父项预算识别码', models.BigIntegerField(null=True)),
                ('预算名称', models.CharField(max_length=255, null=True, unique=True)),
                ('预算周期', models.CharField(max_length=255, null=True, unique=True)),
                ('预算总额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('预算备注', models.TextField(null=True)),
            ],
            options={
                'ordering': ['预算识别码'],
                'verbose_name': '预算信息表',
                'db_table': 'TABEL_预算信息',
            },
        ),
        migrations.CreateModel(
            name='table_Payment',
            fields=[
                ('付款识别码', models.BigAutoField(primary_key=True, serialize=False)),
                ('付款登记时间', models.DateField(null=True)),
                ('付款支付时间', models.DateField(null=True)),
                ('立项识别码', models.BigIntegerField(null=True)),
                ('合同识别码', models.BigIntegerField(null=True)),
                ('付款事由', models.TextField(null=True)),
                ('付款单位识别码', models.BigIntegerField(null=True)),
                ('收款单位识别码', models.BigIntegerField(null=True)),
                ('预算识别码', models.BigIntegerField(null=True)),
                ('付款时预算总额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时项目概算', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时合同付款上限', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时合同值', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时预算余额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时概算余额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时合同可付余额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时合同未付额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时预算已付额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时合同已付额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时概算已付额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款时形象进度', models.TextField(null=True)),
                ('本次付款额', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('付款备注', models.TextField(null=True)),
            ],
            options={
                'ordering': ['付款识别码'],
                'verbose_name': '付款信息表',
                'db_table': 'TABEL_付款信息',
            },
        ),
        migrations.CreateModel(
            name='table_SubContract',
            fields=[
                ('分包合同识别码', models.BigAutoField(primary_key=True, serialize=False)),
                ('立项识别码', models.BigIntegerField(null=True)),
                ('合同识别码', models.BigIntegerField(null=True)),
                ('分包合同编号', models.CharField(max_length=255, null=True, unique=True)),
                ('分包合同名称', models.CharField(max_length=255, null=True, unique=True)),
                ('分包合同主要内容', models.CharField(max_length=255, null=True, unique=True)),
                ('分包合同类别', models.CharField(max_length=255, null=True, unique=True)),
                ('甲方识别码', models.BigIntegerField(null=True)),
                ('乙方识别码', models.BigIntegerField(null=True)),
                ('丙方识别码', models.BigIntegerField(null=True)),
                ('丁方识别码', models.BigIntegerField(null=True)),
                ('分包合同签订时间', models.DateField(null=True)),
                ('分包合同值_签订时', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('分包合同值_最新值', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('分包合同值_最终值', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('分包合同备注', models.TextField(null=True)),
            ],
            options={
                'ordering': ['分包合同识别码'],
                'verbose_name': '分包合同信息表',
                'db_table': 'TABEL_分包合同信息',
            },
        ),
        migrations.AlterField(
            model_name='table_contract',
            name='形象进度',
            field=models.TextField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='table_budget',
            unique_together=set([('预算名称', '预算周期')]),
        ),
    ]
