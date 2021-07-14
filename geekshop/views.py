from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'geekshop/index.html')

def index(request):
    return render(request, 'geekshop/index.html')

def contacts(request):
    return render(request, 'geekshop/contact.html')
