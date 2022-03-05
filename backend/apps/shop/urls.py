from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='index_url'),
    path('products/', ProductListView.as_view(), name='products_list_url'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail_url'),
    path('category_list/<str:category_slug>/', ProductListView.as_view(), name="category_list"),
    path("product_review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path("reviews/<int:pk>/", ReviewsView.as_view(), name="review"),
]
