# Generated by Django 2.0 on 2018-09-18 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0023_auto_20180918_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='data_publicacao',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.RemoveField(
            model_name='favorito',
            name='audio',
        ),
        migrations.AddField(
            model_name='favorito',
            name='audio',
            field=models.ManyToManyField(to='channel.Audio'),
        ),
        migrations.AlterField(
            model_name='feeddeslike',
            name='data_do_feed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='feedlike',
            name='data_do_feed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='historico',
            name='audio',
        ),
        migrations.AddField(
            model_name='historico',
            name='audio',
            field=models.ManyToManyField(to='channel.Audio'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='ultima_atualizacao',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='data',
            field=models.DateTimeField(auto_now=True),
        ),
    ]