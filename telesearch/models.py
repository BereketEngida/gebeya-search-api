from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.operations import BtreeGinExtension
# product model


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    related_name = models.TextField("Related Name", blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            GinIndex(name='NewCatnGinIndex', fields=['name', 'related_name'], opclasses=[
                     'gin_trgm_ops', 'gin_trgm_ops']),
        ]

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    username = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/channel', blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True)
    channel_link = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'channels'
        indexes = [
            GinIndex(name='NewChanGinIndex', fields=['name', 'description'], opclasses=[
                     'gin_trgm_ops', 'gin_trgm_ops']),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='product', on_delete=models.CASCADE)
    channel = models.ForeignKey(
        Channel, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    orginal_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=100, db_index=True, blank=True)
    product_link = models.URLField(blank=True)

    class Meta:
        indexes = [
            GinIndex(name='NewGinIndex', fields=['title', 'description'], opclasses=[
                     'gin_trgm_ops', 'gin_trgm_ops']),
        ]
        verbose_name_plural = 'products'
        ordering = ['-created_date']

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=1, related_name="product_images")
    image = models.ImageField(
        upload_to='images/product', blank=True, null=True)
