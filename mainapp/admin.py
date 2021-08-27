from django.contrib import admin
from .models import ProductCategory, Product
from basketapp.models import Basket

# Register your models here.
# admin.site.register(mainapp_productcategory)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Basket)
