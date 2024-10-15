# Generated by Django 5.0 on 2024-01-02 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order365', '0002_configurations_domainingestion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='ipWhois',
        ),
        migrations.RemoveField(
            model_name='file',
            name='ipswitches',
        ),
        migrations.AddField(
            model_name='folder',
            name='ipWhois',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='privledgeActiveUser',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='threatIp',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='userActive',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='userList',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='userSignCount',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='dataDoct',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]