# Generated by Django 2.2.9 on 2021-01-16 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20210116_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='stock_type',
            field=models.CharField(choices=[('daily', 'DAILY'), ('weekly', 'WEEKLY'), ('monthly', 'RESOLVED')], default='monthly', max_length=50),
        ),
    ]
