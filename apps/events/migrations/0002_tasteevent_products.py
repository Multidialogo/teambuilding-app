# Generated by Django 3.2.9 on 2022-01-06 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasteevent',
            name='products',
            field=models.ManyToManyField(to='products.Product', verbose_name='Products'),
        ),
    ]