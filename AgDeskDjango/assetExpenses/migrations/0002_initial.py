# Generated by Django 5.0.4 on 2025-04-09 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assetExpenses', '0001_initial'),
        ('assetMaintenance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='MaintenanceID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assetMaintenance.maintenance'),
        ),
    ]
