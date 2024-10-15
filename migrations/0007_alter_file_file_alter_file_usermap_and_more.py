# Generated by Django 5.0 on 2024-01-05 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order365', '0006_file_ipwhois_file_privledgeactiveuser_file_threatip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, upload_to='./static/order365/uploads/'),
        ),
        migrations.AlterField(
            model_name='file',
            name='userMap',
            field=models.FileField(blank=True, upload_to='./static/order365/maps/'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='userMap',
            field=models.FileField(blank=True, upload_to='./static/order365/maps/'),
        ),
    ]
