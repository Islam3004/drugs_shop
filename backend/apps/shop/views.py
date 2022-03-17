
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, CreateView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from backend.apps.cart.forms import CartAddProductForm
from backend.apps.cart.cart import Cart
from .models import Products, Reviews, Categories, RatingStar
from .forms import ReviewsForm

# Create your views here.
class HomeView(ListView):
    template_name = 'index.html'
    model = Products
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_products = Products.objects.filter(status=True)
        products_with_discount = Products.objects.order_by('-discount')
        for product in new_products:
            product.price_with_discount = float(product.price) - (float(product.price)*(product.discount/100)) if product.discount else 0
        for product in products_with_discount:
            product.price_with_discount = float(product.price) - (float(product.price)*(product.discount/100)) if product.discount else 0
        context["new_products"] = new_products[:10] if len(new_products) > 10 else new_products
        context["products_with_discount"] = products_with_discount
        return context
    
    

class ProductListView(ListView):
    template_name = 'store.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self, **kwargs):
        category_slug = self.kwargs.get("category_slug")
        search_query = self.request.GET.get("q", '')
        if search_query:
            queryset = self.model.objects.filter(title__icontains=self.request.GET.get("q", ''))
            return queryset
        if category_slug:
            category = get_object_or_404(Categories, slug=category_slug)
            queryset = self.model.objects.filter(status=True, category=category)
            return queryset
        queryset = self.model.objects.filter(status=True)
        for product in queryset:
            product.price_with_discount = float(product.price) - (float(product.price)*(product.discount/100)) if product.discount else 0
        return queryset
    

    



def product_detail(request, slug):
    product = Products.objects.get(slug=slug, status=True)
    if request.method == "GET":
        related_product = Products.objects.filter(status=True, category=product.category)
        reviews = Reviews.objects.select_related('product').filter(product=product.id)

        paginator = Paginator(reviews, 5)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''
        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        context = {
            'product': product, 
            'related_product': related_product,
            'reviews': reviews,
            'form': CartAddProductForm,
            'star_form': ReviewsForm,
            'price_with_discount': float(product.price) - (float(product.price)*(product.discount/100)) if product.discount else 0,
            'page_object': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,

        }
        return render(request, 'product.html', context=context)
    
    elif request.method == "POST":
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['quantity']
            if data <= 0:
                return redirect('product_detail_url', product.slug)
            cart = Cart(request)
            cart.add(product=product, quantity=form.cleaned_data.get('quantity'), update_quantity=form.cleaned_data.get('update'))
            return redirect('product_detail_url', product.slug)



class AddReview(CreateView):
    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        product = Products.objects.get(id=pk)
        rating = RatingStar.objects.get(value=int(request.POST.get('star')))
        if request.user.is_authenticated:
            if form.is_valid():
                Reviews.objects.create(
                    email=request.POST.get('email'),
                    name=request.POST.get('name'),
                    product=product,
                    text=request.POST.get('text'),
                    star=rating,
                )
            return redirect("product_detail_url", product.slug)
        return redirect("login")



def add_favorites(request, id):
    product = get_object_or_404(Products, id=id)
    if request.user.is_authenticated:
        if request.user not in product.favorites.all():
            product.favorites.add(request.user)
            return redirect("index_url")
        else:
            product.favorites.remove(request.user)
            return redirect("index_url")
    return redirect("login")



def get_favorites_product(request):
    if request.user.is_authenticated:
        favorites = Products.objects.filter(favorites=request.user)
        context = {
            'favorites':favorites
        }
        return render(request, 'favorites.html', context=context)
    else:
        return redirect('login')









