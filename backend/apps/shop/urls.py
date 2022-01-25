from django.urls import path, include
from backend.apps.shop import views
urlpatterns = [
    path('', views.AboutView.as_view(), name='index'),
]
