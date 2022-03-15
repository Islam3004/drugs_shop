from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, FormView
from backend.apps.shop.models import Products
from .forms import CartAddProductForm, CheckoutForm
from .cart import Cart
from .models import Order, OrderItem

# Create your views here.

def CartPageView(request):
    cart = Cart(request)
    context = {'cart': cart, 'number_of_cart': len(cart),}
    return context


def cart_add(request, product_id):
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Products.objects.get(id=product_id)
        cart.add(product=product, quantity=1, update_quantity=False)
        return redirect('products_list_url')
    else:
        return redirect('login')

def cart_remove(request, product_id):
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Products.objects.get(id=product_id)
        cart.remove(product=product)
        return redirect('products_list_url')
    else:
        return redirect('login')

def cart_clear(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        cart.clear()
        return redirect('products_list_url')
    else:
        return redirect('login')

class CheckoutView(FormView):
    template_name = 'checkout.html'
    form_class = CheckoutForm

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        order.total_sum = cart.get_total_price()
        order.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                quantity=item['quantity'],
                price=item['price'],
                product=item['product']
            )
            product = Products.objects.get(id=item['product'].id)
            product.quantity - item['quantity']
            product.save()
        cart.clear()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("index_url")

