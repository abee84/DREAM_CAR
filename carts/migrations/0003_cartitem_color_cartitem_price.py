# Generated by Django 4.1.2 on 2022-11-14 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_alter_cart_cart_id_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='color',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.IntegerField(default=True),
        ),
    ]
