# Generated by Django 5.0.1 on 2024-02-09 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0021_remove_reference_dc_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reference',
            name='keyword_1',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='keyword_2',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='keyword_3',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='keyword_4',
        ),
    ]
