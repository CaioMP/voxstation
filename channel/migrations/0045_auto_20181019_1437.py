# Generated by Django 2.0 on 2018-10-19 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0044_auto_20181017_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='visibilidade',
            field=models.CharField(choices=[('publico', 'publico'), ('privado', 'privado')], default='publico', max_length=20),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='visibilidade',
            field=models.CharField(choices=[('publico', 'publico'), ('privado', 'privado')], default='publico', max_length=20),
        ),
    ]