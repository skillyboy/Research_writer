# Generated by Django 4.1 on 2023-03-28 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aiwriter', '0008_delete_mymodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='field',
            old_name='field',
            new_name='name',
        ),
    ]
