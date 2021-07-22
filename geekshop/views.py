from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'geekshop/index.html')

def index(request):
    context = {
        'slogan': 'горячее предложение',
        'user2': 123,
    }
    return render(request, 'geekshop/index.html', context)

def contacts(request):
    return render(request, 'geekshop/contact.html')
