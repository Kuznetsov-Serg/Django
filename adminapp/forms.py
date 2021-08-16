from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm

from authapp.models import ShopUser
from django.forms import ModelChoiceField, CharField
from mainapp.models import ProductCategory, Product


class ShopUserChangePasswordForm(UserCreationForm):
# class ShopUserChangePasswordForm1(PasswordChangeForm):
    class Meta:
        model = ShopUser
        fields = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ShopUserChangePasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super(ProductCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ('is_active', 'category',)
        exclude = ('is_active',)
        # widgets = {'category': CharField(attrs={'disabled': True}),}

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            # if field_name == 'category':
                # field.widget.attrs['style'] = 'visibility: hidden'    # спрятать (сохранение работает)
                # field.widget.attrs['disabled'] = True                 # недоступен для редактирования

    #     initial = getattr(self, 'initial', None)
    #     if initial and initial['category']:
    #         self.fields['category'].widget.attrs['disabled'] = True
    #
    # def clean_category(self):
    #     initial = getattr(self, 'initial', None)
    #     if initial and initial['category']:
    #         return initial['category']
    #     else:
    #         return self.cleaned_data['category']
