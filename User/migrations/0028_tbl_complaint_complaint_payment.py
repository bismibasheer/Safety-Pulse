# Generated by Django 5.1.5 on 2025-04-03 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0027_tbl_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_complaint',
            name='complaint_payment',
            field=models.IntegerField(default=0),
        ),
    ]
