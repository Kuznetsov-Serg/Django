# coding: utf8

from django.db import models
from django.conf import settings
from mainapp.models import Product

# Create your models here.

class Basket(models.Model):
    # user = models.ForeignKey(ShopUser)                  # идентично
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )
    add_time = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.product.name})'

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    @property
    def product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        items = Basket.objects.filter(user=self.user)
        totalquantity = sum(list(map(lambda x: x.quantity, items)))
        return totalquantity

    @property
    def total_cost(self):
        items = Basket.objects.filter(user=self.user)
        totalcost = sum(list(map(lambda x: x.product_cost, items)))
        return totalcost

    @property
    def basket_dict(self):
        basket_dict = {}
        items = Basket.objects.filter(user=self.user)
        for el in items:
            basket_dict[el.product.id] = el.quantity
        return basket_dict

    @classmethod
    def product_quantity_in_basket(self, product=0):
        item = Basket.objects.filter(user=self.user, product=product)
        if (item):
            quantity = item.quantity
        else:
            quantity = 0
        return quantity