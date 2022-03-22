from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, FormView
from backend.apps.shop.models import Products
from .forms import CartAddProductForm, CheckoutForm
from .cart import Cart
from .models import Order, OrderItem

# Create your views here.
def CartPageView(request):
    cart = Cart(request)
    context = {'cart': cart, 'number_of_cart': len(cart)}
    if request.user.is_authenticated:
        favorites = Products.objects.filter(favorites=request.user)
        for product in favorites:
            product.price_with_discount = float(product.price) - (float(product.price)*(product.discount/100)) if product.discount else 0
        context['favorites'] = favorites
        context['favorites_products'] = favorites[:3] if len(favorites) > 3 else favorites
    return context

def add_cart_from_form(request, slug):
    cart = Cart(request)
    product = Products.objects.get(slug=slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data['quantity']
        if data <= 0:
            return redirect('cart_url')
        cart.add(
            product=product,
            quantity=form.cleaned_data.get('quantity'),
            update_quantity=form.cleaned_data.get('update')
        )
        return redirect('cart_url')
    return redirect('cart_url')

def get_cart(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'],
                         'update': True
                         }
            )
        context = {'cart': cart}
        return render(request, 'cart.html', context=context)
    else:
        return redirect('login')

def cart_add(request, product_id):
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Products.objects.get(id=product_id)
        cart.add(product=product)
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
        order.user = self.request.user
        order.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                quantity=item['quantity'],
                price=item['price'],
                product=item['product']
            )
            product = Products.objects.get(id=item['product'].id)
            
        cart.clear()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("index_url")

