from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from datetime import timedelta

from mainapp.models import Product
from ordersapp.models import OrderItem

from adminapp.views import db_profile_by_type


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(
        #     Q(category__name='прочее') |
        #     Q(category__name='дом')
        # )
        # print(len(test_products))
        # db_profile_by_type('learn_db','', connection.queries)

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)
        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
                              Q(order__updated__lte=F('order__created') + action_2__time_delta)
        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition, then=F('product__price') * F('quantity') * action_1__discount)
        action_2__price = When(action_2__condition, then=F('product__price') * F('quantity') * -action_2__discount)
        action_expired__price = When(action_expired__condition, then=F('product__price') * F('quantity') \
                                                                     * action_expired__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        for orderitem in test_orders:
            print(f'{orderitem.action_order:2}| заказ №{orderitem.pk:4}| '
                  f'{orderitem.product.name:20}| скидка {abs(orderitem.total_price):9.2f} руб. | '
                  f'{str(orderitem.order.updated - orderitem.order.created)[:8]}')

