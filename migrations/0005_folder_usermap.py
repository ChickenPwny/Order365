# Generated by Django 5.0 on 2024-01-03 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order365', '0004_folder_userlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='userMap',
            field=models.FileField(blank=True, upload_to='order365/maps/'),
        ),
    ]
