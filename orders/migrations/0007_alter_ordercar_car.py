# Generated by Django 4.1.2 on 2022-11-25 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_alter_car_id'),
        ('orders', '0006_ordercar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercar',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.car'),
        ),
    ]
