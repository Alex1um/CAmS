# Generated by Django 3.1.6 on 2021-02-20 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FrontSite', '0001_initial'),
        ('ThemesControl', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='projects',
        ),
        migrations.AddField(
            model_name='theme',
            name='projects',
            field=models.ManyToManyField(related_name='themed_project', to='FrontSite.Projects'),
        ),
    ]