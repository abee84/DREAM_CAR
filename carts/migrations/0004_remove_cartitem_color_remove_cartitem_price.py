# Generated by Django 4.1.2 on 2022-11-14 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cartitem_color_cartitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='color',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='price',
        ),
    ]
