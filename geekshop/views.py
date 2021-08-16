from django.shortcuts import render
# from mainapp.views import get_basket

# Create your views here.

def main(request):
    return render(request, 'geekshop/index.html')

def index(request):
    title = 'магазин'
    context = {
        'title': title,
        'slogan': 'горячее предложение',
        # 'basket': get_basket(request.user),
    }
    return render(request, 'geekshop/index.html', context)

def contacts(request):
    title = 'контакты'
    context = {
        'title': title,
        # 'basket': get_basket(request.user),
    }
    return render(request, 'geekshop/contact.html', context)
