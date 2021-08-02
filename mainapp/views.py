import random

from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket

from django.urls import reverse


def get_absolute_url(self):
    return reverse('products', kwargs={'category_id': self.category_id})

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).\
                                    exclude(pk=hot_product.pk)[:3]
    return same_products


def products(request, pk=None):
    # pk - вх. параметр для страницы products (фильтр для показа related products) если=None - пункт "ВСЕ"
    title = 'продукты'
    links_menu = ProductCategory.objects.all()      # Считаем все категории из справочника ("все" сформируем в HTML)
    basket = get_basket(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все'}
            products = Product.objects.all().order_by('name')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.all().filter(category__pk=pk).order_by('name')
    else:
        pk = 0
        category = ''
        products = ''

    context = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'category_id': pk,
        'hot_product': hot_product,
        'related_products': same_products,
        'products': products,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk=None):
    title = 'продукт'
    links_menu = ProductCategory.objects.all()      # Считаем все категории из справочника ("все" сформируем в HTML)
    basket = get_basket(request.user)

    product = get_object_or_404(Product, pk=pk)
    same_products = get_same_products(product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': same_products,
        'product': product,
        'basket': basket,
    }
    return render(request, 'mainapp/product.html', context)
