from django.urls import path
from .views import *


urlpatterns = [
    path('add/<int:product_id>', cart_add, name='add_cart_url'),
    path('addf/<int:product_id>', cart_add_from_form, name='add_cart_form_url'),
    path('remove/<int:product_id>', cart_remove, name='remove_cart_url'),
    path('clear/', cart_clear, name='clear_cart_url'), 
    path('checkout/', CheckoutView.as_view(), name='checkout_url')
]