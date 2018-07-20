# Generated by Django 2.0 on 2018-07-16 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_auto_20180712_2105'),
        ('channel', '0002_auto_20180713_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanalPlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_home', models.BooleanField(default=False)),
                ('canal', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='canal_playlists', to='account.Canal')),
            ],
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='proprietarios',
        ),
        migrations.AddField(
            model_name='playlist',
            name='proprietarios',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='playlist_proprietario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='canalplay',
            name='playlist',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Playlist_canais', to='channel.Playlist'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='canal',
            field=models.ManyToManyField(default=None, related_name='canal_playlist', through='channel.CanalPlay', to='account.Canal'),
        ),
    ]