from django import forms
from .models import Order
from django.core.exceptions import ValidationError


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control", "style":"width:60px;"}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    
    

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['fio', 'phone_number', 'email', 'address', 'post_code', 'bank_card']

        widgets = {
            'fio': forms.TextInput(attrs = {'placeholder': 'Нуржигит Чыныбаев Нурматович', 'class': 'input'}),
            'email': forms.EmailInput(attrs = {'placeholder': 'nurzhigit@example.com', 'class': 'input'}),
            'phone_number': forms.TextInput(attrs = {'placeholder': '+996 700 514 927', 'class': 'input'}),
            'address': forms.TextInput(attrs = {'placeholder': 'Бишкек, ул. Аблесова, дом 78А', 'class': 'input'}),
            'post_code': forms.TextInput(attrs = {'placeholder': '1111', 'class': 'input'}),
            'bank_card': forms.TextInput(attrs = {'placeholder': '1111 1111 1111 1111', 'class': 'input'})
        }