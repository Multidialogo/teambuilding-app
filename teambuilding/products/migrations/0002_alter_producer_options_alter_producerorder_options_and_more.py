# Generated by Django 4.0.1 on 2022-01-10 17:26

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producer',
            options={'ordering': ['name'], 'verbose_name': 'producer', 'verbose_name_plural': 'producers'},
        ),
        migrations.AlterModelOptions(
            name='producerorder',
            options={'verbose_name': 'cumulative order to producer', 'verbose_name_plural': 'cumulative orders to producers'},
        ),
        migrations.AlterModelOptions(
            name='producerorderdeliveryaddress',
            options={'verbose_name': 'delivery address', 'verbose_name_plural': 'delivery addresses'},
        ),
        migrations.AlterModelOptions(
            name='producerpostaladdress',
            options={'verbose_name': 'postal address', 'verbose_name_plural': 'postal addresses'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title'], 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.AlterModelOptions(
            name='productorder',
            options={'ordering': ['producer', 'product'], 'verbose_name': 'simple order', 'verbose_name_plural': 'simple orders'},
        ),
        migrations.AlterModelOptions(
            name='productpurchaseoption',
            options={'ordering': ['price_cents'], 'verbose_name': 'purchase option', 'verbose_name_plural': 'purchase options'},
        ),
        migrations.AlterField(
            model_name='producer',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='producer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='producer',
            name='postal_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='producer', to='products.producerpostaladdress', verbose_name='postal address'),
        ),
        migrations.AlterField(
            model_name='producerorder',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='products.producerorderdeliveryaddress', verbose_name='delivery address'),
        ),
        migrations.AlterField(
            model_name='producerorder',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producer_order', to='products.producer', verbose_name='producer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=100, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producer', verbose_name='producer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.user', verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='products.producer', verbose_name='producer'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='producer_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='products.producerorder', verbose_name='in cumulative order'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='products.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='purchase_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='products.productpurchaseoption', verbose_name='purchase option'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('PROCESSED', 'Processed')], default='CREATED', max_length=10, verbose_name='order status'),
        ),
        migrations.AlterField(
            model_name='productpurchaseoption',
            name='amount',
            field=models.CharField(max_length=50, verbose_name='amount'),
        ),
        migrations.AlterField(
            model_name='productpurchaseoption',
            name='price_cents',
            field=models.IntegerField(verbose_name='price EUR (cents)'),
        ),
        migrations.AlterField(
            model_name='productpurchaseoption',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_option', to='products.product', verbose_name='product'),
        ),
    ]