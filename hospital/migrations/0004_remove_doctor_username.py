# Generated by Django 4.2.5 on 2023-11-24 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_alter_doctor_phone_number_alter_doctor_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='username',
        ),
    ]
