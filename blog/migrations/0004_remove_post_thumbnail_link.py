# Generated by Django 3.2.11 on 2022-02-09 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_tags_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='thumbnail_link',
        ),
    ]
