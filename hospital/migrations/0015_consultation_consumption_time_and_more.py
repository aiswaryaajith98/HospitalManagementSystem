# Generated by Django 4.2.5 on 2023-11-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0014_consultation'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='consumption_time',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='consultation',
            name='medicine_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
