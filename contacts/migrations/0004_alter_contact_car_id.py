# Generated by Django 4.1.2 on 2022-11-25 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_alter_contact_car_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='car_id',
            field=models.IntegerField(),
        ),
    ]
