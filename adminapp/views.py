from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.admin.forms import AdminPasswordChangeForm

from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, DetailView, UpdateView, FormView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from authapp.forms import ShopUserCreateForm, ShopUserEditForm
from adminapp.forms import ShopUserChangePasswordForm, ProductCategoryForm, ProductForm


# @user_passes_test(lambda u: u.is_superuser)
# def users(request, page=1):
#     title = 'админка/пользователи'
#     user_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', 'username')
#
#     paginator = Paginator(user_list, 5)
#     try:
#         objects_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         objects_paginator = paginator.page(1)
#     except EmptyPage:
#         objects_paginator = paginator.page(paginator.num_pages)
#
#     context = {
#         'title': title,
#         'objects': objects_paginator
#     }
#     return render(request, 'adminapp/users.html', context)

class UserListView(LoginRequiredMixin, ListView):
    model = ShopUser  # единственный обязательный параметр
    template_name = 'adminapp/users.html'  # по умолчанию - 'adminapp/ShopUser_list.html'
    context_object_name = 'objects'  # по умолчанию...
    paginate_by = 5

    def get_queryset(self):  # для сортировки
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', 'username')

    def get_context_data(self):
        context = super(UserListView, self).get_context_data()
        title = 'админка/пользователи'
        context['title'] = title
        # context.update({'title': title})    # идентично
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'админка/создание пользователя'
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users_page', args='1'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'type_operation': 'создание',
#         'update_form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', context)

class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    form_class = ShopUserCreateForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self):
        context = super(UserCreateView, self).get_context_data()
        title = 'админка/создание пользователя'
        type_operation = 'создать'
        context.update({'title': title, 'type_operation': type_operation})
        # context.update({'title': title})
        # context.update({'type_operation': type_operation})
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'админка/изменение пользователя'
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = ShopUserEditForm(request.POST, request.FILES, instance=user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users_page', args='1'))
#     else:
#         user_form = ShopUserEditForm(instance=user)
#
#     context = {
#         'title': title,
#         'type_operation': 'изменение',
#         'user_avatar': user.avatar,
#         'form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', context)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    form_class = ShopUserEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self):
        context = super(UserUpdateView, self).get_context_data()
        title = 'админка/изменение пользователя'
        type_operation = 'изменить'
        user = get_object_or_404(ShopUser, pk=self.kwargs['pk'])
        context.update({'title': title, 'type_operation': type_operation, 'user_avatar': user.avatar})
        return context


# def user_update_password(request, pk=1):
#     title = 'Смена пароля'
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         password_form = ShopUserChangePasswordForm(request.POST, request.FILES, instance=user)
#         if password_form.is_valid():
#             password_form.save()
#
#             return HttpResponseRedirect(reverse('admin_staff:users_page', args='1'))
#     else:
#         password_form = ShopUserChangePasswordForm(instance=user)
#     context = {
#         'title': title,
#         'user_avatar': user.avatar,
#         'password_form': password_form
#     }
#     return render(request, 'adminapp/password.html', context)

class UserUpdatePassword(LoginRequiredMixin, PasswordChangeView):
    model = ShopUser
    # form_class = AdminPasswordChangeForm
    template_name = 'adminapp/password.html'
    success_url = reverse_lazy('admin_staff:users')
    #
    # def get_context_data(self):
    #     context = super(UserUpdateView, self).get_context_data()
    #     title = 'админка/изменение пользователя'
    #     type_operation = 'изменить'
    #     user = get_object_or_404(ShopUser, pk=self.kwargs['pk'])
    #     context.update({'title': title, 'type_operation': type_operation, 'user_avatar': user.avatar})
    #     return context


class UserUpdatePassword1(LoginRequiredMixin, FormView):
    model = ShopUser
    form_class = PasswordChangeForm
    template_name = 'adminapp/password.html'
    success_url = reverse_lazy('admin_staff:users')
    template_name = 'password_change.html'

    def get_form_kwargs(self):
        kwargs = super(UserUpdatePassword, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        # update_session_auth_hash(self.request, form.user)
        return super(UserUpdatePassword, self).form_valid(form)


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'админка/удаление пользователя'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         user.is_active = False if user.is_active else True
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users_page', args='1'))
#     else:
#         user_form = ShopUserEditForm(instance=user)
#
#     type_operation = 'удалить пользователя' if user.is_active else 'восстановить активность'
#     context = {
#         'title': title,
#         'type_operation': type_operation,
#         'user_avatar': user.avatar,
#         'update_form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', context)

class UserDeleteView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    form_class = ShopUserEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self):
        context = super(UserDeleteView, self).get_context_data()
        title = 'админка/деактивация пользователя'
        user = get_object_or_404(ShopUser, pk=self.kwargs['pk'])
        type_operation = 'деактивировать' if user.is_active else 'активировать'
        context.update({'title': title, 'type_operation': type_operation, 'user_avatar': user.avatar})
        return context

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(ShopUser, pk=self.kwargs['pk'])
        user.is_active = False if user.is_active else True
        user.save()
        # self.object = self.get_object()
        return super().post(request, *args, **kwargs)



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
def products(request, pk, page=1):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category__pk=pk).order_by('-is_active', 'name')

    paginator = Paginator(products, 5)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'category': category,
        'objects': products_paginator,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукты/создание'
    category = get_object_or_404(ProductCategory, pk=pk)
    type_operation = 'создать'

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductForm(initial={'category': category})

    context = {
        'title': title,
        'type_operation': type_operation,
        'update_form': product_form
    }
    return render(request, 'adminapp/product_update.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукты/подробно'
#     product = get_object_or_404(Product, pk=pk)
#     type_operation = 'просмотр (подробно)'
#
#     context = {
#         'title': title,
#         'type_operation': type_operation,
#         'product': product
#     }
#     return render(request, 'adminapp/product_read.html', context)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'  # по умолчанию - 'adminapp/Product_detail.html'


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукты/редактирование'
    type_operation = 'изменить'
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))
    else:
        product_form = ProductForm(instance=product)

    context = {
        'title': title,
        'type_operation': type_operation,
        'update_form': product_form,
        'category': product.category
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        # product.delete()
        product.is_active = False if product.is_active else True
        product.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[product.category.pk]))
