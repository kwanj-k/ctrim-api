# Generated by Django 2.1.3 on 2019-01-27 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190127_0726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ttags',
            new_name='tags',
        ),
    ]
