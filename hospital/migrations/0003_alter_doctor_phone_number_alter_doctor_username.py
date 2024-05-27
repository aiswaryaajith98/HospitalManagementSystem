# Generated by Django 4.2.5 on 2023-11-24 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_doctor_email_doctor_phone_number_doctor_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='phone_number',
            field=models.CharField(default='N/A', max_length=15),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='username',
            field=models.CharField(default='default_username', max_length=30, unique=True),
        ),
    ]
