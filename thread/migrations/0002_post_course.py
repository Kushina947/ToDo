# Generated by Django 5.1.1 on 2024-10-30 06:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0001_initial'),
        ('thread', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lecture.course'),
            preserve_default=False,
        ),
    ]