# Generated by Django 4.1.2 on 2022-11-25 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_contact_car_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='car_id',
            field=models.IntegerField(blank=True),
        ),
    ]
