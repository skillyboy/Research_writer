# Generated by Django 4.1 on 2023-03-08 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiwriter', '0002_chapter_content_field_index_research_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='field',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
