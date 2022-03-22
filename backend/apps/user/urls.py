from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import RegisterPage
from .views import CustomLoginView
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index_url'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
]

