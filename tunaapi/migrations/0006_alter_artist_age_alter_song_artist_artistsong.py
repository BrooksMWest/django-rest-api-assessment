# Generated by Django 4.2.16 on 2024-12-10 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tunaapi', '0005_rename_artist_id_song_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='tunaapi.artist'),
        ),
        migrations.CreateModel(
            name='ArtistSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tunaapi.artist')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tunaapi.song')),
            ],
        ),
    ]
