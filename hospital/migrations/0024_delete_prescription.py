# Generated by Django 4.2.5 on 2023-11-26 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0023_reassignment_delete_reassignmentrequest'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Prescription',
        ),
    ]
