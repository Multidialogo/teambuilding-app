# Generated by Django 3.2.9 on 2021-12-21 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('postal_address', '0002_data_migration'),
        ('orders', '0002_order_pricebyquantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProducerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producer')),
            ],
        ),
        migrations.CreateModel(
            name='ProducerOrderDeliveryAddress',
            fields=[
                ('postaladdress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='postal_address.postaladdress')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.producerorder')),
            ],
            bases=('postal_address.postaladdress',),
        ),
        migrations.AddField(
            model_name='order',
            name='producerOrder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.producerorder'),
        ),
    ]
