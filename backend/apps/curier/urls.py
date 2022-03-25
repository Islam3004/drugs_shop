from django.urls import path
from .views import *

urlpatterns = [
    path('', order_list_view, name='order_list_url'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail_url'),
    path('sent/<int:id>', sent_order, name='sent_order')

]