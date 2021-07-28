from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket
from django.urls import reverse


# Create your views here.

# def index(request):
#     return render(request, 'mainapp/products.html')
#
# def products(request):
#     return render(request, 'mainapp/products.html')
def get_absolute_url(self):
    return reverse('products', kwargs={'category_id': self.category_id})

def products(request, pk=None):
    # pk - вх. параметр для страницы products (фильтр для показа related products) если=None - пункт "ВСЕ"
    title = 'продукты'

    links_menu = ProductCategory.objects.all()      # Считаем все категории из справочника ("все" сформируем в HTML)
    # links_menu = [{'href': '/products/category/0/', 'id': 0, 'name': 'все'}]  # дополним пунктом меню для всех категорий
    # for el in ProductCategory.objects.all():                        # Считаем все категории из справочника
    #     links_menu.append({'href': '/products/category/'+str(el.id)+'/', 'id': el.id, 'name': el.name})

    products = Product.objects.all()[:3]                # Считаем продукты из справочника
    # products = Product.objects.all()    # Считаем продукты из справочника (количество уже ограничим в форме)
    # products = []
    # products_amount = {}
    # for el in Product.objects.all():
    #     if products_amount.get(el.category_id) == None:     # не было такой категории
    #         products_amount[el.category_id] = 0
    #     if products_amount[el.category_id] < 3:             # берем не более трех товаров каждой категории
    #         products_amount[el.category_id] += 1
    #         products.append(el)

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        basket_sum = 0
        for el in basket:
            basket_sum += el.quantity * el.product.price
    else:
        basket = []
        basket_sum = 0

    # basket = Basket.objects.all()

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

    context = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'category_id': pk,
        'products': products,
        'related_products': products,
        'basket': basket,
        'basket_sum': basket_sum,
    }
    return render(request, 'mainapp/products.html', context)
