# Generated by Django 4.2.16 on 2024-12-04 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tunaapi', '0002_rename_album_song_album_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='album_id',
            new_name='album',
        ),
    ]