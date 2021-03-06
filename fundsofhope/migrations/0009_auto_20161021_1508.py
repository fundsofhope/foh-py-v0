# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-21 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fundsofhope', '0008_project_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default=b'images/default/no-img.jpg', upload_to=b'_upload_path')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='photo',
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
        migrations.AddField(
            model_name='projectpicture',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fundsofhope.Project'),
        ),
    ]
