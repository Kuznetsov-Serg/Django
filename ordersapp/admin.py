from django.contrib import admin

from .models import Order, OrderItem

# admin.site.register(Order)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "updated", "status")
    list_filter = ('created', 'user')

# admin.site.register(OrderItem)