# Generated by Django 5.0.4 on 2025-04-01 07:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('FarmAcc', '0001_initial'),
        ('Tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assignedTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='farmID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FarmAcc.farminfo'),
        ),
        migrations.AddField(
            model_name='kanbancontents',
            name='taskID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tasks.task'),
        ),
    ]
