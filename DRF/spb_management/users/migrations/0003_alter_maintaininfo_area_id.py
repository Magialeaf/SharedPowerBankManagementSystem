# Generated by Django 5.0.4 on 2024-04-22 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0001_initial'),
        ('users', '0002_maintaininfo_aid_maintaininfo_area_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintaininfo',
            name='area_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maintain_info', to='areas.areainfo', verbose_name='area_id'),
        ),
    ]
