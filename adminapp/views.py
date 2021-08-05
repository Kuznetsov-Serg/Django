from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from adminapp.forms import ShopUserChangePasswordForm, ProductCategoryForm

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'
    user_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', 'username')
    context = {
        'title': title,
        'objects': user_list
    }
    return render(request, 'adminapp/users.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'админка/создание пользователя'
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'type_operation': 'создание',
        'update_form': user_form
    }
    return render(request, 'adminapp/user_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'админка/изменение пользователя'
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserEditForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserEditForm(instance=user)

    context = {
        'title': title,
        'type_operation': 'изменение',
        'user_avatar': user.avatar,
        'update_form': user_form
    }
    return render(request, 'adminapp/user_update.html', context)

def user_update_password(request, pk=1):
    title = 'Смена пароля'
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        password_form = ShopUserChangePasswordForm(request.POST, request.FILES, instance=user)
        if password_form.is_valid():
            password_form.save()

            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        password_form = ShopUserChangePasswordForm(instance=user)
    context = {
        'title': title,
        'user_avatar': user.avatar,
        'password_form': password_form
    }
    return render(request, 'adminapp/password.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'админка/удаление пользователя'

    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False if user.is_active else True
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserEditForm(instance=user)

    type_operation = 'удалить пользователя' if user.is_active else 'восстановить активность'
    context = {
        'title': title,
        'type_operation': type_operation,
        'user_avatar': user.avatar,
        'update_form': user_form
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all().order_by('-is_active', 'name')
    content = {
        'title': title,
        'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'админка/создание категории'

    if request.method == 'POST':
        category_form = ProductCategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryForm()

    context = {
        'title': title,
        'type_operation': 'создание',
        'update_form': category_form
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'админка/изменение категории'

    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryForm(request.POST, request.FILES, instance=category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryForm(instance=category)

    context = {
        'title': title,
        'type_operation': 'изменение',
        'update_form': category_form
    }
    return render(request, 'adminapp/category_update.html', context)



@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'админка/удаление категории'

    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        # category.delete()
        # вместо удаления лучше сделаем неактивным
        category.is_active = False if category.is_active else True
        category.save()
        return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryForm(instance=category)

    type_operation = 'удалить категорию' if category.is_active else 'восстановить категорию'
    context = {
        'title': title,
        'type_operation': type_operation,
        'update_form': category_form
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('-is_active', 'name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    pass