# Generated by Django 5.0.4 on 2024-04-21 06:48

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('areas', '0001_initial'),
        ('merchants', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowerBankInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(default='新充电宝', max_length=20, verbose_name='名称')),
                ('img', models.ImageField(blank=True, default='default.png', upload_to='media/images/power_bank_img/', verbose_name='图片')),
                ('status', models.SmallIntegerField(choices=[(0, '空闲'), (1, '充电中'), (2, '已借出'), (3, '已损坏'), (4, '已报废')], default=0, verbose_name='状态')),
                ('hourly_fee', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='每小时费用')),
                ('electricity_percentage', models.IntegerField(default=100, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='电量百分比')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='areas.areainfo', verbose_name='区域')),
                ('merchant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='merchants.merchantinfo', verbose_name='商户')),
            ],
        ),
        migrations.CreateModel(
            name='PowerBankMaintenance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('finished', models.BooleanField(default=False, verbose_name='是否完成')),
                ('date', models.DateTimeField(verbose_name='处理日期')),
                ('question_description', models.CharField(max_length=50, verbose_name='问题描述')),
                ('maintenance_result', models.CharField(max_length=50, verbose_name='处理结果')),
                ('maintainer_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.accountinfo', verbose_name='运维人员')),
                ('power_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='power_bank.powerbankinfo', verbose_name='充电宝')),
            ],
        ),
    ]
