# Generated by Django 4.0.2 on 2022-03-05 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_articleclass_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CategoryArticleClass',
            new_name='CategoryClass',
        ),
    ]
