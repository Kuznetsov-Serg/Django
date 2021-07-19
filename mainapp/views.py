from django.shortcuts import render
import json

# Create your views here.

# def index(request):
#     return render(request, 'mainapp/products.html')
#
# def products(request):
#     return render(request, 'mainapp/products.html')

def index(request):
    # write_links_menu_to_JSON_file()

    title = 'каталог'
    links_menu = read_json('./geekshop/templates/geekshop/links_menu.JSON')     # считаем перечень меню из JSON-файла

    # links_menu = [
    #     {'href': 'index', 'name': 'все!!!'},
    #     {'href': 'products_home', 'name': 'дом'},
    #     {'href': 'products_office', 'name': 'офис'},
    #     {'href': 'products_modern', 'name': 'модерн'},
    #     {'href': 'products_classic', 'name': 'классика'},
    # ]

    context = {
        'title': title,
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', context)

################################################
# Вспомогательные функции для работы с файлами
################################################

def read_file(path):
    file = open(path, "r")
    data = file.read()
    file.close()
    return data


def read_json(path):
    return json.loads(read_file(path))


def write_json(path, data):
    return write_file(path, json.dumps(data))


def write_file(path, data):
    file = open(path, "w")
    file.write(str(data))
    file.close()
    return data

# Функция записи в первый раз в JSON-файл перечня меню
def write_links_menu_to_JSON_file ():
    json_data = [
        {'href': 'index', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    write_json('./geekshop/templates/geekshop/links_menu.JSON', json_data);
