# Generated by Django 4.1.7 on 2023-02-15 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='convict',
            new_name='perp',
        ),
    ]
