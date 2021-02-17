# Generated by Django 3.1.2 on 2020-11-21 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(choices=[('warning', 'Out of date'), ('success', 'Up to date'), ('danger', 'Edited')], default='danger', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Home_markdown', models.TextField(blank=True, default=None, null=True)),
                ('Home_html', models.TextField(blank=True, default=None, null=True)),
                ('Relations', models.TextField(blank=True, default=None, null=True)),
                ('AllowedUsers', models.ManyToManyField(blank=True, related_name='permitted', to=settings.AUTH_USER_MODEL)),
                ('Creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('Owners', models.ManyToManyField(related_name='owners', to=settings.AUTH_USER_MODEL)),
                ('Parents', models.ManyToManyField(blank=True, related_name='dependent', through='FrontSite.Dependence', to='FrontSite.Projects')),
            ],
        ),
        migrations.AddField(
            model_name='dependence',
            name='Dependence',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dependencies', to='FrontSite.projects'),
        ),
        migrations.AddField(
            model_name='dependence',
            name='Parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent', to='FrontSite.projects'),
        ),
    ]
