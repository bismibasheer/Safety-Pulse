# Generated by Django 5.1.5 on 2025-02-14 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Guest', '0018_tbl_mvd'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_file', models.FileField(upload_to='Assets/Articlefile/photo/')),
                ('article_date', models.DateField(auto_now_add=True)),
                ('article_description', models.CharField(max_length=30)),
                ('MVD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_mvd')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(upload_to='Assets/Videofile/photo/')),
                ('video_date', models.DateField(auto_now_add=True)),
                ('video_description', models.CharField(max_length=30)),
                ('MVD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_mvd')),
            ],
        ),
    ]
