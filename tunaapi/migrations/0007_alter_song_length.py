# Generated by Django 4.2.16 on 2024-12-10 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunaapi', '0006_alter_artist_age_alter_song_artist_artistsong'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='length',
            field=models.IntegerField(max_length=50),
        ),
    ]