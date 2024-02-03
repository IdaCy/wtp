# Generated by Django 5.0.1 on 2024-02-03 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0017_alter_reference_ref_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='approval_status',
            field=models.CharField(blank=True, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20, null=True),
        ),
    ]
