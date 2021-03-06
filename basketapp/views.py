# coding="utf-8"
from django.db import connection

from adminapp.views import db_profile_by_type

coding: "utf8"

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from mainapp.models import Product
from .models import Basket

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.template.loader import render_to_string
from django.http import JsonResponse

from django.db.models import F, Q


@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    context = {
        'title': title,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    # basket = Basket.objects.filter(user=request.user, product=product).first()
    basket = Basket.objects.filter(user__id=request.user.id, product__id=pk).select_related('product').first()

    if not basket:      # Еще не было корзины - создадим
        product = get_object_or_404(Product, pk=pk)
        basket = Basket(user=request.user, product=product)
        basket.quantity = 1
    else:
        basket.quantity += 1
        # basket.quantity = F('quantity') + 1     # F - только для обновления существующих значений
    basket.save()

    db_profile_by_type('Basket', 'UPDATE', connection.queries)

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))     # чтобы вернуться не на login
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        context = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', context)

        return JsonResponse({'result': result})
