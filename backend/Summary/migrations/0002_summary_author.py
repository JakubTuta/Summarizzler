# Generated by Django 5.1.5 on 2025-02-06 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Summary', '0001_initial'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='summaries', to='Users.userdata'),
            preserve_default=False,
        ),
    ]
