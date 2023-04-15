# Generated by Django 4.1 on 2023-03-13 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aiwriter', '0006_content_created_at_alter_content_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=150, null=True)),
                ('company_uuid', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('url', models.URLField(null=True)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'company',
                'db_table': 'company',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_field', tinymce.models.HTMLField()),
            ],
        ),
        migrations.AddField(
            model_name='research',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='research',
            name='body',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ProfileDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=150, null=True)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=150, null=True)),
                ('date_joined', models.DateTimeField(blank=True, null=True)),
                ('p_img', models.ImageField(blank=True, default='profile/avatar.png', null=True, upload_to='profile')),
                ('username', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profileDetail',
                'verbose_name_plural': 'profileDetails',
                'db_table': 'profiledetail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DemoUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, null=True)),
                ('last_name', models.CharField(max_length=150, null=True)),
                ('fullname', models.CharField(max_length=150, null=True)),
                ('url', models.URLField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.CharField(max_length=150, null=True)),
                ('date_joined', models.DateTimeField(blank=True, null=True)),
                ('date_expired', models.DateTimeField(blank=True, null=True)),
                ('profile_pic', models.ImageField(default='default.jpg', upload_to='')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aiwriter.company')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'demouser',
                'verbose_name_plural': 'demo profiles',
                'db_table': 'demouser',
                'managed': True,
            },
        ),
    ]
