from django import forms
from .models import Order

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone_number', 'email', 'address', 'post_code', 'bank_card']

        widgets = {
            'name': forms.TextInput(attrs = {'placeholder': 'Нуржигит', 'class': 'input'}),
            'email': forms.EmailInput(attrs = {'placeholder': 'nurzhigit@example.com', 'class': 'input'}),
            'phone_number': forms.TextInput(attrs = {'placeholder': '+996 700 514 927', 'class': 'input'}),
            'address': forms.TextInput(attrs = {'placeholder': 'Бишкек, ул. Аблесова, дом 78А', 'class': 'input'}),
            'post_code': forms.TextInput(attrs = {'placeholder': '1111', 'class': 'input'}),
            'bank_card': forms.TextInput(attrs = {'placeholder': '1111 1111 1111 1111', 'class': 'input'})
        }