from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.core.mail import send_mail
from django.conf import settings
from authapp.models import ShopUser, ShopUserProfile

from .forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm, ShopUserChangePasswordForm, \
    ShopUserProfileEditForm
from .models import ShopUser


def login(request):
    title = 'входа'

    login_form = ShopUserLoginForm(data=request.POST or None)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение отправлено')
            else:
                print('сообщение НЕ отправлено!!!')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)

@transaction.atomic
@login_required
def edit(request):
    title = 'профиль'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            # profile_form.save()       # не требуется
            return HttpResponseRedirect(reverse('index'))
            # return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/edit.html', context)


def password(request):
    title = 'Смена пароля'

    if request.method == 'POST':
        password_form = ShopUserChangePasswordForm(request.POST, request.FILES, instance=request.user)
        if password_form.is_valid():
            password_form.save()

            return HttpResponseRedirect(reverse('index'))
    else:
        password_form = ShopUserChangePasswordForm(instance=request.user)
    context = {
        'title': title,
        'password_form': password_form
    }
    return render(request, 'authapp/password.html', context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
            {settings.DOMAIN_NAME} перейдите по ссылке: \n' \
              f'<a href="{settings.DOMAIN_NAME}{verify_link}">Активировать</a>'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            # auth.login(request, user)
            # 'You have multiple authentication backends configured and therefore must provide the `backend` argument
            # or set the `backend` attribute on the user.'
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user.username}')
        return render(request, 'authapp/verification.html')
    except Exception as err:
        print(f'error activation user : {err.args}')
        return HttpResponseRedirect(reverse('index'))


# def save_user_from_telegram(request, *args, **kwargs):
#     try:
#         data = request.GET
#         if data['username'] and data['id']:
#             username = f"{data['username']} (telegram_id:{data['id']})"
#             # user = ShopUser.objects.get(username=username)
#             # user = ShopUser.objects.all().filter(username=username)
#             user = get_object_or_404(ShopUser, username=username)
#     except Exception as err:
#         user = ShopUser(
#             username=username,
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             avatar=data['photo_url'],
#         )
#         user.save()
#
#     auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#     if 'next' in request.POST.keys():
#         return HttpResponseRedirect(request.POST['next'])
#     else:
#         return HttpResponseRedirect(reverse('index'))
#
#     return HttpResponseRedirect(reverse('index'))


def telegram_login(request, *args, **kwargs):
    try:
        data = request.GET
        if data['username'] and data['id']:
            username = f"{data['username']} (telegram_id:{data['id']})"
            # user = ShopUser.objects.get(username=username)
            # user = ShopUser.objects.all().filter(username=username)
            user = get_object_or_404(ShopUser, username=username)
    except Exception as err:
        user = ShopUser(
            username=username,
            first_name=data['first_name'],
            last_name=data['last_name'],
            avatar=data['photo_url'],
        )
        user.save()

    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return HttpResponseRedirect(reverse('index'))
