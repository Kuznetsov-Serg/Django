from django.urls import path, re_path, include
from django.views.generic import TemplateView

from .views import login, logout, register, edit, password, verify, telegram_login

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    # re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', verify, name='verify'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
    # path('complete/telegram/', save_user_from_telegram, name='save_user_from_telegram'),
    path('telegram_login/', telegram_login, name='telegram_login'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('auth/', include('social_django.urls', namespace='social')),
]
