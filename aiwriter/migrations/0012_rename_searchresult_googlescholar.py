# Generated by Django 4.1 on 2023-04-01 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aiwriter', '0011_remove_file_user_alter_file_date_created'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SearchResult',
            new_name='GoogleScholar',
        ),
    ]