# Generated by Django 3.2.5 on 2021-08-18 14:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0010_auto_20210818_1053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopuserprofile',
            old_name='aboutMe',
            new_name='about_me',
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 20, 14, 40, 7, 421648)),
        ),
    ]
