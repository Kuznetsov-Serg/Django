from django.shortcuts import render
from .models import ProductCategory, Product
from django.urls import reverse


# Create your views here.

# def index(request):
#     return render(request, 'mainapp/products.html')
#
# def products(request):
#     return render(request, 'mainapp/products.html')
def get_absolute_url(self):
    return reverse('products', kwargs={'category_id': self.category_id})

def index(request, category_id=0):
    # category_id - вх. параметр для страницы products (фильтр для показа related products) если=0 - пункт "ВСЕ"

    # write_links_menu_to_JSON_file()
    # fill_new_bd_from_EXCEL_file()               # Зальем новую БД с перечнем товаров и категорий (запускаем при изменении Excel-файла)

    title = 'каталог'
    # Вариант статической загрузки категорий
    # links_menu = [
    #     {'href': 'index', 'name': 'все!!!'},
    #     {'href': 'products_home', 'name': 'дом'},
    #     {'href': 'products_office', 'name': 'офис'},
    #     {'href': 'products_modern', 'name': 'модерн'},
    #     {'href': 'products_classic', 'name': 'классика'},
    # ]

    # Вариант загрузки категорий из JSON-файла
    # links_menu = read_json('./links_menu.JSON')     # считаем перечень меню из JSON-файла (раньше)

    # Вариант загрузки категорий из БД (таблица ProductsCategory)
    # links_menu = ProductCategory.objects.all()      # Считаем все категории из справочника (не получим "все")
    links_menu = [{'href': '/products0/', 'id': 0, 'name': 'все'}]  # дополним пунктом меню для всех категорий
    for el in ProductCategory.objects.all():                        # Считаем все категории из справочника
        links_menu.append({'href': '/products'+str(el.id)+'/', 'id': el.id, 'name': el.name})

    # products = Product.objects.all()[:3]                # Считаем продукты из справочника
    # products = Product.objects.all()    # Считаем продукты из справочника (количество уже ограничим в форме)
    products = []
    products_amount = {}
    for el in Product.objects.all():
        if products_amount.get(el.category_id) == None:     # не было такой категории
            products_amount[el.category_id] = 0
        if products_amount[el.category_id] < 3:             # берем не более трех товаров каждой категории
            products_amount[el.category_id] += 1
            products.append(el)

    # print(f'category_id= {category_id}')
    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': products,
        'category_id': category_id,
    }
    return render(request, 'mainapp/products.html', context)

