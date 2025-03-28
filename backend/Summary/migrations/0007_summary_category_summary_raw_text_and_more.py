# Generated by Django 5.1.5 on 2025-02-13 17:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Summary', '0006_summary_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='category',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='summary',
            name='raw_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='summary',
            name='content_type',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='summary',
            name='dislikes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='summary',
            name='favorites',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='summary',
            name='is_private',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='summary',
            name='likes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='summary',
            name='summary',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='summary',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='summary',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='summary',
            name='url',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='summary',
            name='user_prompt',
            field=models.TextField(default=''),
        ),
    ]
