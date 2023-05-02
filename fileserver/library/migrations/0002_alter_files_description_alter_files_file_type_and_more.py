# Generated by Django 4.2 on 2023-04-28 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='description',
            field=models.CharField(blank=True, help_text='description', max_length=255),
        ),
        migrations.AlterField(
            model_name='files',
            name='file_type',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='files',
            name='file_url',
            field=models.CharField(blank=True, help_text='url', max_length=255),
        ),
        migrations.AlterField(
            model_name='filetracker',
            name='downloads',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='filetracker',
            name='emails',
            field=models.IntegerField(default=0),
        ),
    ]
