from django.urls import path
from .views import products, product, products_ajax
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    # path('category/<int:pk>/ajax/', cache_page(3600)(products_ajax)),
    path('category/<int:pk>/page/<int:page>/', cache_page(3600)(products), name='page'),
    # path('category/<int:pk>/page/<int:page>/ajax/', cache_page(3600)(products_ajax)),
    path('product/<int:pk>/', product, name='product'),

]
