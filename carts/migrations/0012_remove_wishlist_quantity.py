# Generated by Django 4.1.2 on 2022-12-06 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0011_wishlist_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='quantity',
        ),
    ]