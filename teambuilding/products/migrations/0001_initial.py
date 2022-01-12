# Generated by Django 4.0.1 on 2022-01-12 18:35

from django.db import migrations, models
import django.db.models.deletion
import lib.phonenumber.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('postaladdress', '0002_data'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('phone', lib.phonenumber.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='phone number')),
                ('added_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='added by')),
            ],
            options={
                'verbose_name': 'producer',
                'verbose_name_plural': 'producers',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProducerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'cumulative order to producer',
                'verbose_name_plural': 'cumulative orders to producers',
            },
        ),
        migrations.CreateModel(
            name='ProducerOrderDeliveryAddress',
            fields=[
                ('postaladdress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='postaladdress.postaladdress')),
            ],
            options={
                'verbose_name': 'delivery address',
                'verbose_name_plural': 'delivery addresses',
            },
            bases=('postaladdress.postaladdress',),
        ),
        migrations.CreateModel(
            name='ProducerPostalAddress',
            fields=[
                ('postaladdress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='postaladdress.postaladdress')),
            ],
            options={
                'verbose_name': 'postal address',
                'verbose_name_plural': 'postal addresses',
            },
            bases=('postaladdress.postaladdress',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('description', models.CharField(max_length=100, verbose_name='description')),
                ('added_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='added by')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producer', verbose_name='producer')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ProductPurchaseOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_cents', models.IntegerField(verbose_name='price EUR (cents)')),
                ('amount', models.CharField(max_length=50, verbose_name='amount')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_option', to='products.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'purchase option',
                'verbose_name_plural': 'purchase options',
                'ordering': ['price_cents'],
                'unique_together': {('amount', 'product')},
            },
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('PROCESSED', 'Processed')], default='CREATED', max_length=10, verbose_name='order status')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.user', verbose_name='customer')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='products.producer', verbose_name='producer')),
                ('producer_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='products.producerorder', verbose_name='in cumulative order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='products.product', verbose_name='product')),
                ('purchase_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='products.productpurchaseoption', verbose_name='purchase option')),
            ],
            options={
                'verbose_name': 'simple order',
                'verbose_name_plural': 'simple orders',
                'ordering': ['producer', 'product'],
            },
        ),
        migrations.AddField(
            model_name='producerorder',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='products.producerorderdeliveryaddress', verbose_name='delivery address'),
        ),
        migrations.AddField(
            model_name='producerorder',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producer_order', to='products.producer', verbose_name='producer'),
        ),
        migrations.AddField(
            model_name='producer',
            name='postal_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='producer', to='products.producerpostaladdress', verbose_name='postal address'),
        ),
    ]
