from django.urls import path
from .views import *


urlpatterns = [
    path('', get_cart, name='cart_url'),
    path('add/<int:product_id>', cart_add, name='add_cart_url'),
    path('add_from_form/<str:slug>', add_cart_from_form, name='add_cart_from_form'),
    path('remove/<int:product_id>', cart_remove, name='remove_cart_url'),
    path('clear/', cart_clear, name='clear_cart_url'),
    path('checkout/', CheckoutView.as_view(), name='checkout_url')

]

