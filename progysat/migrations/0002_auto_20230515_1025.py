# Generated by Django 3.2.19 on 2023-05-15 08:25

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('progysat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='types',
        ),
        migrations.RemoveField(
            model_name='contactpage',
            name='newsletter_text',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='profiles',
        ),
        migrations.AlterField(
            model_name='homepage',
            name='resources_block_explication',
            field=wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Explication du bloc des ressources'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='resources_block_title',
            field=models.CharField(blank=True, default='Liste des ressources', max_length=64, verbose_name='Titre du bloc des ressources'),
        ),
        migrations.DeleteModel(
            name='NewsLetterSettings',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
