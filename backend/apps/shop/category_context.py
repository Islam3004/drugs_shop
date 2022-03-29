from .models import Categories, Products
from backend.apps.cart.models import Order

def get_category(request):
    category = Categories.objects.all()
    context = {"categories":category}
    if request.user.is_authenticated:
        context['order'] = Order.objects.filter(user=request.user)
    return context

