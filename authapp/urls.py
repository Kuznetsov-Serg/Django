from django.urls import path, re_path
from .views import login, logout, register, edit, password, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    # re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', verify, name='verify'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
