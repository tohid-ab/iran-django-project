# Generated by Django 4.0.2 on 2022-02-28 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_djangotricks'),
    ]

    operations = [
        migrations.CreateModel(
            name='AskedQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='سوال')),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ('created',),
            },
        ),
        migrations.AlterModelOptions(
            name='articleclass',
            options={'ordering': ('created',), 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterModelOptions(
            name='djangotricks',
            options={'ordering': ('created',), 'verbose_name': 'Video', 'verbose_name_plural': 'Videos'},
        ),
    ]
