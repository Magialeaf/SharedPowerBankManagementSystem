# Generated by Django 5.0.4 on 2024-05-04 05:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_powerbankrentalinfo_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='powerbankfeeinfo',
            name='pay_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='支付时间'),
            preserve_default=False,
        ),
    ]
