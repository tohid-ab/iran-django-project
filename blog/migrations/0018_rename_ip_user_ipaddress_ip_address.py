# Generated by Django 4.0.2 on 2022-04-06 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_ipaddress_articleclass_visits'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ipaddress',
            old_name='ip_user',
            new_name='ip_address',
        ),
    ]
