# Generated by Django 2.1.7 on 2019-07-14 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='store',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='user_ptr',
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
    ]
