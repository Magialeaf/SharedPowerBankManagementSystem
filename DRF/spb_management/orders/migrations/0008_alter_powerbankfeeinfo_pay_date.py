# Generated by Django 5.0.4 on 2024-05-04 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_powerbankfeeinfo_pay_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='powerbankfeeinfo',
            name='pay_date',
            field=models.DateTimeField(null=True, verbose_name='支付时间'),
        ),
    ]
