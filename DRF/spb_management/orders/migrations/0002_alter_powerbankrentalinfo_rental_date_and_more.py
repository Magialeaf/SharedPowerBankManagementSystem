# Generated by Django 5.0.4 on 2024-05-01 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='powerbankrentalinfo',
            name='rental_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='开始时间'),
        ),
        migrations.AlterField(
            model_name='powerbankreturninfo',
            name='return_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='归还时间'),
        ),
    ]
