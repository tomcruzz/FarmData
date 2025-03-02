# Generated by Django 5.0.4 on 2025-02-17 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assetMaintenance', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenance',
            name='maintenaceType',
        ),
        migrations.AddField(
            model_name='maintenance',
            name='maintenanceType',
            field=models.PositiveIntegerField(choices=[(0, 'General'), (1, 'Scheduled Service'), (2, 'Inspection'), (3, 'Repair')], default=0),
        ),
    ]
