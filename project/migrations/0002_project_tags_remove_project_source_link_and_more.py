# Generated by Django 4.2.4 on 2023-09-02 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='project.tag'),
        ),
        migrations.RemoveField(
            model_name='project',
            name='source_link',
        ),
        migrations.AddField(
            model_name='project',
            name='source_link',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]