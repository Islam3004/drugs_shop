# Generated by Django 3.2.9 on 2022-02-20 21:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0006_auto_20220220_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]