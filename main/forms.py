from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, regist, buy_curs
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')
        widgets = {
            'username': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваш username'
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваш пароль'
            }),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        widgets = {
            'username': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваш username'
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваш пароль'
            }),
            }


class registform(ModelForm):
    class Meta:
        model = regist
        fields = ['username', 'name', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш никнейм'
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваш email'
            }),
            'password1': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите пароль',
            }),
            'password2': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль',
            })
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['username'] == '':
            raise forms.ValidationError('Вы должны указать свой username')
        elif CustomUser.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('Пользователь с таким username существует!')
        elif CustomUser.objects.filter(email=cd['email']).exists() and CustomUser.objects.filter(email=cd['email']).first().is_active:
            raise forms.ValidationError('Пользователь с таким email существует!')
        elif cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        elif len(cd['password1']) < 6 or len(cd['password2']) < 6:
            raise forms.ValidationError('Пароль должен быть больше 6 сиволов')
        return cd['password2']


class byu_cursForm(ModelForm):
    class Meta:
        model = buy_curs
        fields = ['name', 'price']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш никнейм'
            }),
            'price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
        }