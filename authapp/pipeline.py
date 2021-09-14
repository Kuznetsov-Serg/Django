import hashlib
from django.conf import settings

from collections import OrderedDict
from urllib.parse import urlunparse, urlencode, urlparse
from social_core.exceptions import AuthForbidden
import requests
from datetime import datetime
from django.utils import timezone

from .models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https', 'api.vk.com', '/method/users.get', None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200_orig')),
                                                    access_token=response['access_token'], v='5.89')),
                              None))
        resp = requests.get(api_url)
        if resp.status_code != 200:
            return
        data = resp.json()['response'][0]
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.about_me = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        if data['photo_200_orig']:
            user.avatar = data['photo_200_orig']

        user.save()
    elif backend.name == 'odnoklassniki-oauth2':
        # https://apiok.ru/dev/methods/rest/users/users.getInfo
        # https://apiok.ru/dev/methods/rest/users/users.getCurrentUser
        # API выполняется, но возвращает не больше уже имеющегося, поэтому можно закомментировать и все взять в response
        param_api = 'application_key=' + settings.SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME +\
            'fields=first_name,last_name,gender,email,age,birthday,pic600x600,current_statusformat=jsonmethod=users.getCurrentUser'

        secret_key = hashlib.md5((response['access_token'] + settings.SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET).encode('utf8')).hexdigest()
        sig = hashlib.md5((param_api + secret_key).encode('utf8')).hexdigest()

        api_url = urlunparse(('https', 'api.ok.ru', '/api/users/getCurrentUser', None,
                              urlencode(OrderedDict(application_key=settings.SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME,
                                                    fields=','.join((
                                                                    'first_name', 'last_name', 'gender', 'email', 'age',
                                                                    'birthday', 'pic600x600', 'current_status')),
                                                    format='json', method='users.getCurrentUser', sig=sig,
                                                    access_token=response['access_token'])),
                              None))
        resp = requests.get(api_url)
        if resp.status_code != 200:
            return
        data = resp.json()
        if data['gender']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['gender'] == 'male' else ShopUserProfile.FEMALE

        if data['current_status']:
            user.shopuserprofile.about_me = data['current_status']

        if data['age']:
            age = data['age']
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        if response['pic_3']:
            user.avatar = response['pic_3']

        user.save()

    elif backend.name == 'telegram':
        param_api = 'application_key=' + settings.SOCIAL_AUTH_TELEGRAM_BOT_TOKEN + \
                    'fields=first_name,last_name,gender,email,age,birthday,pic600x600,current_statusformat=jsonmethod=users.getCurrentUser'

        secret_key = hashlib.md5((response['access_token'] + settings.SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET).encode('utf8')).hexdigest()
        sig = hashlib.md5((param_api + secret_key).encode('utf8')).hexdigest()

        api_url = urlunparse(('https', 'api.ok.ru', '/api/users/getCurrentUser', None,
                              urlencode(OrderedDict(application_key=settings.SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME,
                                                    fields=','.join((
                                                        'first_name', 'last_name', 'gender', 'email', 'age',
                                                        'birthday', 'pic600x600', 'current_status')),
                                                    format='json', method='users.getCurrentUser', sig=sig,
                                                    access_token=response['access_token'])),
                              None))
        resp = requests.get(api_url)
        if resp.status_code != 200:
            return
        data = resp.json()
        if data['gender']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['gender'] == 'male' else ShopUserProfile.FEMALE

        if data['current_status']:
            user.shopuserprofile.about_me = data['current_status']

        if data['age']:
            age = data['age']
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        if response['pic_3']:
            user.avatar = response['pic_3']

        user.save()