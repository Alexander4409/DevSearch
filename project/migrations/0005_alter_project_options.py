# Generated by Django 4.2.4 on 2023-10-07 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_project_image_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total']},
        ),
    ]
