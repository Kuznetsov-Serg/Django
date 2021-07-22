from django.urls import path
from .views import index

app_name = 'mainapp'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index, name='index'),
]
