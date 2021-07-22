from django.contrib import admin
from .models import ProductCategory, Product

# Register your models here.
# admin.site.register(mainapp_productcategory)
admin.site.register(ProductCategory)
admin.site.register(Product)
