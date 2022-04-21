# Generated by Django 4.0.2 on 2022-03-07 21:35

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_djangoroadmap_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleclass',
            name='description',
            field=models.TextField(null=True, verbose_name='متن مقاله'),
        ),
        migrations.AlterField(
            model_name='articleclass',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='article/%Y/%m/%d', verbose_name='عکس'),
        ),
        migrations.AlterField(
            model_name='articleclass',
            name='slug',
            field=models.SlugField(max_length=255, null=True, verbose_name='لینک'),
        ),
        migrations.AlterField(
            model_name='articleclass',
            name='title',
            field=models.CharField(max_length=255, null=True, verbose_name='عنوان مقاله'),
        ),
        migrations.AlterField(
            model_name='djangoroadmap',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
