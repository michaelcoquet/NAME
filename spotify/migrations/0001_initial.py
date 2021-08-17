# Generated by Django 3.2.4 on 2021-08-08 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.CharField(max_length=62, primary_key=True, serialize=False)),
                ('data', models.JSONField()),
                ('feature', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.CharField(max_length=62, primary_key=True, serialize=False)),
                ('data', models.JSONField()),
                ('tracks', models.ManyToManyField(related_name='album_tracks', to='spotify.Track')),
            ],
        ),
    ]
