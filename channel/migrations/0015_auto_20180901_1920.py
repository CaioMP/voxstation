# Generated by Django 2.0 on 2018-09-01 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0014_resposta_audio_comentado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='deslikes',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='likes',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='deslikes',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='likes',
            field=models.IntegerField(null=True),
        ),
    ]
