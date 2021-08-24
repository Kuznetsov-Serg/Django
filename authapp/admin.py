from django.contrib import admin

from authapp.models import ShopUser

# admin.site.register(ShopUser)
@admin.register(ShopUser)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name",)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    # list_filter = ('created', 'user')