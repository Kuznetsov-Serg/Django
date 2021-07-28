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
