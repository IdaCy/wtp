# Generated by Django 5.0.1 on 2024-03-06 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0027_remove_user_firstname_remove_user_lastname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='company',
            new_name='organisation',
        ),
    ]
