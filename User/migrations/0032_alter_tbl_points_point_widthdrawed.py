# Generated by Django 5.2 on 2025-04-28 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0031_alter_tbl_points_point_credited_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_points',
            name='point_widthdrawed',
            field=models.IntegerField(default=0),
        ),
    ]
