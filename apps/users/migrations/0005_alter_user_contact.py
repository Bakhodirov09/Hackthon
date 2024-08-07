# Generated by Django 5.0.7 on 2024-08-05 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.contact', verbose_name='Telegram-аккаунт'),
        ),
    ]
