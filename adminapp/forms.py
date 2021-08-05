from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm


from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

class ShopUserChangePasswordForm(PasswordChangeForm):
    pass

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
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
