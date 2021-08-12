from django.urls import path
from .views import (
    # users,
    UserListView,
    # user_create,
    UserCreateView,
    # user_update,
    UserUpdateView,
    # user_update_password,
    UserUpdatePassword,
    # user_delete,
    UserDeleteView,
    categories,
    category_create,
    category_update,
    category_delete,
    products,
    product_create,
    # product_read,
    ProductDetailView,
    product_update,
    product_delete,
)
# from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView

app_name = 'adminapp'

urlpatterns = [
    # path('users/read/', users, name='users'),
    # path('users/read/page/<int:page>/', users, name='users_page'),
    path('users/read/', UserListView.as_view(), name='users'),
    # path('users/create/', user_create, name='user_create'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    # path('users/update/<int:pk>/', user_update, name='user_update'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    # path('users/delete/<int:pk>/', user_delete, name='user_delete'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    # path('users/update/password/<int:pk>/', user_update_password, name='user_update_password'),
    path('users/update/password/<int:pk>/', UserUpdatePassword, name='user_update_password'),
    path('users/update/password/', UserUpdatePassword, name='user_update_password'),

    path('categories/create/', category_create, name='category_create'),
    path('categories/read/', categories, name='categories'),
    path('categories/update/<int:pk>/', category_update, name='category_update'),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),

    path('products/create/category/<int:pk>/', product_create, name='product_create'),
    path('products/read/category/<int:pk>/', products, name='products'),
    path('products/read/category/<int:pk>/page/<int:page>/', products, name='products_page'),
    # path('products/read/<int:pk>/', product_read, name='product_read'),
    path('products/read/<int:pk>/', ProductDetailView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', product_update, name='product_update'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
]
