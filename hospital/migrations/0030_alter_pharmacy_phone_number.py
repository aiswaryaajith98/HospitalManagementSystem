# Generated by Django 4.2.5 on 2023-11-28 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0029_doctor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pharmacy',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
