# Generated by Django 3.2.9 on 2021-12-21 14:03

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('postal_address', '0002_data_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone number')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Title')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producer', verbose_name='Producer')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ProducerPostalAddress',
            fields=[
                ('postaladdress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='postal_address.postaladdress')),
                ('producer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.producer')),
            ],
            bases=('postal_address.postaladdress',),
        ),
        migrations.CreateModel(
            name='ProductPurchaseOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priceInCents', models.IntegerField(verbose_name='Price (cents)')),
                ('quantity', models.CharField(max_length=50, verbose_name='Quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Product')),
            ],
            options={
                'ordering': ['priceInCents'],
                'unique_together': {('quantity', 'product')},
            },
        ),
    ]