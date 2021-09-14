import random

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ProductCategory, Product
from basketapp.models import Basket

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from django.template.loader import render_to_string
from django.http import JsonResponse


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)     # Считаем все категории из справочника ("все" сформируем в HTML)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)       # Считаем все категории из справочника ("все" сформируем в HTML)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category').order_by('name')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category').order_by('name')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_absolute_url(self):
    return reverse('products', kwargs={'category_id': self.category_id})

# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     else:
#         return []

def get_hot_product():
    # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
    products = get_products()
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    # same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    # same_products = Product.objects.filter(is_active=True, category__id=hot_product.category_id).select_related('category').exclude(pk=hot_product.pk)[:3]
    same_products = get_products_in_category_orederd_by_price(hot_product.category_id).exclude(pk=hot_product.pk)[:3]
    return same_products

@cache_page(3600)
def products(request, pk=None, page=1):
    # pk - вх. параметр для страницы products (фильтр для показа related products) если=None - пункт "ВСЕ"
    title = 'продукты'
    # links_menu = ProductCategory.objects.filter(is_active=True)     # Считаем все категории из справочника ("все" сформируем в HTML)
    links_menu = get_links_menu()
    # basket = get_basket(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': pk}
            # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category').order_by('name')
            products = get_products()
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            category = get_category(pk)
            # products = Product.objects.all().filter(category__pk=pk).order_by('name')
            # products = Product.objects.filter(is_active=True, category__is_active=True, category__id=pk).select_related('category').order_by('name')
            products = get_products_in_category_orederd_by_price(pk)
    else:
        pk = 0
        category = ''
        products = ''

    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'category_id': pk,
        'hot_product': hot_product,
        'related_products': same_products,
        'products': products_paginator,
        # 'basket': basket,
    }
    # return render(request, 'mainapp/products_list.html', context)
    return render(request, 'mainapp/products.html', context)


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()

        if pk:
            if pk == '0':
                category = {
                    'pk': 0,
                    'name': 'все'
                }
                products = get_products_orederd_by_price()
            else:
                category = get_category(pk)
                products = get_products_in_category_orederd_by_price(pk)

            paginator = Paginator(products, 3)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string(
                'mainapp/includes/inc_products_list_content.html',
                context=content,
                request=request)

            return JsonResponse({'result': result})


def product(request, pk=None):
    title = 'продукт'
    # links_menu = ProductCategory.objects.filter(is_active=True)     # Считаем все категории из справочника ("все" сформируем в HTML)
    links_menu = get_links_menu()
    # basket = get_basket(request.user)

    # product = get_object_or_404(Product, pk=pk)
    product = get_product(pk)
    same_products = get_same_products(product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': same_products,
        'product': product,
        # 'basket': basket,
    }
    return render(request, 'mainapp/product.html', context)
