# Generated by Django 2.0 on 2018-07-13 19:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedDesLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_do_feed', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_do_feed', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='Audio_feed',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='conta_feed',
        ),
        migrations.RemoveField(
            model_name='audio',
            name='feedback',
        ),
        migrations.RemoveField(
            model_name='audio',
            name='deslikes',
        ),
        migrations.RemoveField(
            model_name='audio',
            name='likes',
        ),
        migrations.DeleteModel(
            name='FeedBack',
        ),
        migrations.AddField(
            model_name='feedlike',
            name='Audio_feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio_do_like', to='channel.Audio'),
        ),
        migrations.AddField(
            model_name='feedlike',
            name='conta_feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conta_do_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feeddeslike',
            name='Audio_feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio_do_deslike', to='channel.Audio'),
        ),
        migrations.AddField(
            model_name='feeddeslike',
            name='conta_feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conta_do_deslike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='audio',
            name='deslikes',
            field=models.ManyToManyField(default=None, related_name='deslikes', through='channel.FeedDesLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='audio',
            name='likes',
            field=models.ManyToManyField(default=None, related_name='likes', through='channel.FeedLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
