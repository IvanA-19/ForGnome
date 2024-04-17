from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['count']
        labels = {'count': 'Количество'}


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address']
        labels = {'address': 'Введите адрес доставки:'}
