# Generated by Django 4.2.16 on 2024-12-04 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tunaapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='album',
            new_name='album_id',
        ),
    ]
