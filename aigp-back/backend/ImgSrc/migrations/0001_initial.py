# Generated by Django 5.0.4 on 2024-04-26 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CustomUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImgInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/goe/', verbose_name='image')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('flag', models.BooleanField(default=False, verbose_name='is_goe')),
                ('username', models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, related_name='imginfos', to='CustomUser.cuser', to_field='username', verbose_name='username')),
            ],
            options={
                'verbose_name': 'uinfo',
                'verbose_name_plural': 'uinfos',
            },
        ),
    ]
