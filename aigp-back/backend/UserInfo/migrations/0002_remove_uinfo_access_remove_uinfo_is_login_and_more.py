# Generated by Django 5.0.4 on 2024-04-26 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uinfo',
            name='access',
        ),
        migrations.RemoveField(
            model_name='uinfo',
            name='is_login',
        ),
        migrations.RemoveField(
            model_name='uinfo',
            name='refresh',
        ),
    ]
