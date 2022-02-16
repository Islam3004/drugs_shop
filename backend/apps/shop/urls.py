from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='index_url'),
    path('products/', ProductListView.as_view(), name='products_list_url'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail_url'),
]
