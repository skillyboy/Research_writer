# Generated by Django 4.1 on 2023-03-30 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiwriter', '0010_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='user',
        ),
        migrations.AlterField(
            model_name='file',
            name='date_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]