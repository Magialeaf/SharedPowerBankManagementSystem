# Generated by Django 5.0.3 on 2024-04-09 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_accountinfo_id_alter_userinfo_username_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='phone_number',
            new_name='phone',
        ),
    ]