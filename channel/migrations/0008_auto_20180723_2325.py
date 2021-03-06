# Generated by Django 2.0 on 2018-07-24 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0007_auto_20180723_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='canalplay',
            name='canal',
        ),
        migrations.RemoveField(
            model_name='canalplay',
            name='playlist',
        ),
        migrations.AlterField(
            model_name='playlist',
            name='canal',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='canal_playlist', to='account.Canal'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='descricao',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='CanalPlay',
        ),
    ]
