# Generated by Django 4.2.5 on 2023-11-25 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0009_remove_prescription_medicine_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='medicine1',
            new_name='medicine_name',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medicine2',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medicine3',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medicine4',
        ),
    ]
