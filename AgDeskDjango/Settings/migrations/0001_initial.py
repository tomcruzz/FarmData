# Generated by Django 5.0.4 on 2025-04-09 14:14

import django.contrib.auth.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('FarmAcc', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='orgSettingsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', models.CharField(max_length=100)),
                ('datetime_format', models.CharField(max_length=100)),
                ('temperature_label', models.CharField(max_length=50)),
                ('mass_label', models.CharField(max_length=50)),
                ('area_label', models.CharField(max_length=50)),
                ('length_label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='internalTeamsModel',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('teamName', models.CharField(max_length=100)),
                ('teamDescription', models.CharField(max_length=1000)),
                ('active', models.BooleanField(default=True)),
                ('teamImage', models.ImageField(default='images/internalTeams/default.jpg', upload_to='images/internalTeams')),
                ('farm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FarmAcc.farminfo')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
    ]
