# Generated by Django 3.2.11 on 2022-02-03 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]
