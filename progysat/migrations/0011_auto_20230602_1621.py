# Generated by Django 3.2.19 on 2023-06-02 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progysat', '0010_auto_20230531_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='body',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='is_global',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='types',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='zones',
        ),
        migrations.AddField(
            model_name='thematic',
            name='color',
            field=models.CharField(default='', max_length=6, verbose_name='code hex de la couleur (ex 000000 pour du blanc)'),
        ),
    ]
