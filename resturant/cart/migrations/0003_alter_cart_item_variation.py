# Generated by Django 4.1.1 on 2022-10-14 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_dishes_model_description_and_more'),
        ('cart', '0002_remove_cart_item_variation_cart_item_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_item',
            name='variation',
            field=models.ManyToManyField(blank=True, to='app.variation'),
        ),
    ]
