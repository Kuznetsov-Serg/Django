from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from mainapp.models import Product
from .models import Basket

# Create your views here.
def basket(reques):
    context = {}
    return render(request, 'basketapp/basket.html', context)

def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:      # Еще не было корзины - создадим
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def basket_remove(request, pk):
    context = {}
    return render(request, 'basketapp/basket.html', context)