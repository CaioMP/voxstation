# Generated by Django 2.0 on 2018-07-20 01:47

import channel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0005_playlist_ultima_atualizacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='capa',
            field=models.ImageField(default=None, null=True, upload_to=channel.models.Playlist.playlist_capa_path),
        ),
    ]