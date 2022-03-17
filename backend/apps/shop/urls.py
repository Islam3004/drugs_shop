from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='index_url'),
    path('box', BoxView.as_view(), name='box'),
    path('car', CarView.as_view(), name='car'),
    path('ship', ShipView.as_view(), name='ship'),
    path('products/', ProductListView.as_view(), name='products_list_url'),
    path('product/<slug:slug>/', product_detail, name='product_detail_url'),
    path('product/favorites/<int:id>/', add_favorites, name='add_favorites'),
    path('category_list/<str:category_slug>/', ProductListView.as_view(), name="category_list"),
    path('product_review/<int:pk>/', AddReview.as_view(), name="add_review"),
    path('favorites', get_favorites_product, name='favorites'),

]
