# Generated by Django 5.1.5 on 2025-02-12 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0012_tbl_user'),
        ('User', '0017_remove_tbl_feedback_user_delete_tbl_complaint_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_user',
            name='place',
        ),
        migrations.DeleteModel(
            name='tbl_Mvd',
        ),
        migrations.DeleteModel(
            name='tbl_User',
        ),
    ]
