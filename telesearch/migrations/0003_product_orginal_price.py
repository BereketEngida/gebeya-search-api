# Generated by Django 4.0.5 on 2022-06-21 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telesearch', '0002_remove_product_posted_date_product_updated_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='orginal_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
