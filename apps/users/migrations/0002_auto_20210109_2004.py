# Generated by Django 2.2.9 on 2021-01-09 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='store',
        ),
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
