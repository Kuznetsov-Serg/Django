from django import template
from django.conf import settings

register = template.Library()

def media_folder_products(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    """
    if not string:
        string = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    """
    if not string:
        string = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='quantity_in_basket')
def quantity_in_basket(product, basket):
    """
    Определяет, сколько конкретного товара уже в корзине
    """
    item = basket.filter(product=product)
    if (item):
        return f'&#22291; {item[0].quantity}шт'
        # return f'в корзине {item[0].quantity}шт'
    else:
        return ''

register.filter('media_folder_products', media_folder_products)
