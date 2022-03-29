from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.
class CustomLoginView(LoginView):
    model = User
    template_name = "login.html"
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('order_list_url')
        return reverse_lazy('products_list_url')

class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('products_list_url')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

