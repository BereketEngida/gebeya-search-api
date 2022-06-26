from itertools import product
from django.contrib import admin
from .models import Category, Channel, Product, ProductImages
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username', 'slug',
                    'description', 'image', 'created_date']
    list_filter = ['created_date']
    prepopulated_fields = {
        'slug': ('name',), }


class ImagesAdmin(admin.StackedInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesAdmin]
    list_display = ['title', 'category', 'channel',
                    'price', 'created_date', 'phone_number', 'slug', 'description', 'updated_date']
    list_filter = ['created_date', 'category', 'channel', 'updated_date']
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = Product


admin.site.register(ProductImages)
admin.site.register(Product, ProductAdmin)
