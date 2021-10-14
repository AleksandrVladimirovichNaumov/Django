from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from products.models import ProductCategory


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class UserAdminProfileForm(UserProfileForm):


    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class CategoryAdminCreateForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryAdminCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание категории'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CategoryAdminUpdateForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryAdminUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'name'
        self.fields['description'].widget.attrs['placeholder'] = 'description'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'