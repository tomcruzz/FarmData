# Generated by Django 5.0.4 on 2025-04-01 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('FarmAcc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmContacts',
            fields=[
                ('farmContactID', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=64)),
                ('image', models.ImageField(default='images/contact_images/defaultImage.png', upload_to='images/contact_images')),
                ('desc', models.CharField(max_length=128)),
                ('deleted', models.BooleanField(default=False)),
                ('farmID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FarmAcc.farminfo')),
            ],
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('contactInfoID', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.PositiveIntegerField()),
                ('field', models.CharField(choices=[('PH', 'Phone'), ('EM', 'Email'), ('AD', 'Address'), ('WB', 'Website'), ('NA', 'Other')], max_length=2)),
                ('info', models.CharField(max_length=64)),
                ('deleted', models.BooleanField(default=False)),
                ('farmContactID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Emergency.farmcontacts')),
            ],
        ),
    ]
