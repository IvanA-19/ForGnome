from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {'username': 'Имя пользователя',
                  'first_name': 'Имя',
                  'last_name': 'Фамилия',
                  'email': 'Электронная почта',
                  'password1': 'Пароль',
                  'password2': 'Подтверждение пароля'}
