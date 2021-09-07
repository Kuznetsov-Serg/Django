# coding: utf8

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product

# Create your models here.

# Класс для возвращения товара в базу при удалении корзины
class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):      # Почему-то не работает!!!
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()    # расширяем опции класса (при delete ваызывается...)

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


    @cached_property
    # @property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        totalquantity = sum(list(map(lambda x: x.quantity, items)))
        return totalquantity

    @property
    def total_cost(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        totalcost = sum(list(map(lambda x: x.product_cost, items)))
        return totalcost

    @property
    def basket_dict(self):
        basket_dict = {}
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        for el in items:
            basket_dict[el.product.id] = el.quantity
        return basket_dict

    @classmethod
    def product_quantity_in_basket(self, product=0):
        items = self.get_items_cached.filter(product=product)
        # item = Basket.objects.filter(user=self.user, product=product)
        if (item):
            quantity = item.quantity
        else:
            quantity = 0
        return quantity

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()


    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)
