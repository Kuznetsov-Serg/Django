from django import template
from django.conf import settings

register = template.Library()

def media_folder_products(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    если это не является ссылкой в интернете http:// https:// и т.д.
    """
    if not string:
        string = 'products_images/default.jpg'
    elif string.name.find(':') != -1:
        return string

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    если это не является ссылкой в интернете http:// https:// и т.д.
    """
    if not string:
        string = 'users_avatars/default.jpg'
    elif string.name.find(':') != -1:
        return string
    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='quantity_in_basket')
def quantity_in_basket(product, basket):
    """
    Определяет, сколько конкретного товара уже в корзине
    """
    if str(type(basket)).find('QuerySet') != -1:    # Basket является QuerySet (пользователь залогинился и корзина есть)
        item = basket.filter(product=product)
        if (item):                                  # Корзина не пустая
            return f'&#22291; {item[0].quantity}шт'
            # return f'в корзине {item[0].quantity}шт'
    return ''

register.filter('media_folder_products', media_folder_products)
