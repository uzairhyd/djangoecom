from django.contrib import admin

from .models import Product
from django.utils.html import format_html

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'featured', 'active', 'image')

    def image(self, obj):
        print(obj)
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image.short_description = 'Image'

    

admin.site.register(Product, ProductAdmin)
