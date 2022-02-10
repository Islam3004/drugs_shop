from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_url'), 
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail_url'),

]
