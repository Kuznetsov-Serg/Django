from django.urls import path
from .views import products, product

app_name = 'mainapp'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('product/<int:pk>/', product, name='product'),
]
