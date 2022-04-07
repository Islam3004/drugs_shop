from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, CreateView, TemplateView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
import statistics
from django.core.paginator import Paginator
import math
from backend.apps.cart.forms import CartAddProductForm
from backend.apps.cart.cart import Cart
from .models import Products, Reviews, Categories, RatingStar
from .forms import ReviewsForm
from decimal import Decimal as D
from django.db.models import Q
from django.http import JsonResponse

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
            product.price_with_discount = float(product.price) - (
                        float(product.price) * (product.discount / 100)) if product.discount else 0
            reviews = Reviews.objects.select_related('product').filter(product=product.id)
            star = 0
            stars = []
            for review in reviews:
                star = review.star.value
                stars.append(star)
            if len(stars) > 1:
                product.simple_star = statistics.mean(stars)
            elif len(stars) == 1:
                product.simple_star = star
            else:
                product.simple_star = 0
        for product in products_with_discount:
            product.price_with_discount = float(product.price) - (
                        float(product.price) * (product.discount / 100)) if product.discount else 0
            reviews = Reviews.objects.select_related('product').filter(product=product.id)
            star = 0
            stars = []
            for review in reviews:
                star = review.star.value
                stars.append(star)
            if len(stars) > 1:
                product.simple_star = statistics.mean(stars)
            elif len(stars) == 1:
                product.simple_star = star
            else:
                product.simple_star = 0
        context["new_products"] = new_products[:10] if len(new_products) > 10 else new_products
        context["products_with_discount"] = products_with_discount[:10] if len(
            products_with_discount) > 10 else products_with_discount
        context["products_with_discount"] = products_with_discount[:10] if len(products_with_discount) > 10 else products_with_discount
        return context

class ProductsListView(ListView):
    template_name = 'store.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self, **kwargs):
        queryset = Products.objects.filter(status=True)
        for product in queryset:
            product.price_with_discount = float(product.price) - (
                    float(product.price) * (product.discount / 100)) if product.discount else 0
        for product in queryset:
            reviews = Reviews.objects.select_related('product').filter(product=product.id)
            star = 0
            stars = []
            for review in reviews:
                star = review.star.value
                stars.append(star)
            if len(stars) > 1:
                product.simple_star = statistics.mean(stars)
            elif len(stars) == 1:
                product.simple_star = star
            else:
                product.simple_star = 0
        return queryset


class ProductListView(ListView):
    template_name = 'store.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 9
    

    def get_queryset(self, **kwargs):
        search_query = self.request.GET.get("q", '')
        filter_price1 = D(self.request.GET.get('price-min', 0))
        filter_price2 = D(self.request.GET.get('price-max', 0))
        if filter_price1 == '':
            filter_price1 = 0
        if filter_price2 == '':
            filter_price2 = Products.objects.aggregate(Max('price'))['price__max']
        else:
            pass
        if search_query:
            queryset = Products.objects.filter(
                    Q(title__icontains=search_query))
        elif self.request.GET.getlist("category"):
            queryset = Products.objects.filter(
                # Q(title__icontains=search_query)
                Q(category_id__in=self.request.GET.getlist("category")) ,
                Q(price__range=(filter_price1, filter_price2)))
        else:
            queryset = Products.objects.filter(
                Q(price__range=(filter_price1, filter_price2)))
        for product in queryset:
            product.price_with_discount = float(product.price) - (
                        float(product.price) * (product.discount / 100)) if product.discount else 0
        for product in queryset:
            reviews = Reviews.objects.select_related('product').filter(product=product.id)
            star = 0
            stars = []
            for review in reviews:
                star = review.star.value
                stars.append(star)
            if len(stars) > 1:
                product.simple_star = statistics.mean(stars)
            elif len(stars) == 1:
                product.simple_star = star
            else:
                product.simple_star = 0
        return queryset


def product_detail(request, slug):
    product = Products.objects.get(slug=slug, status=True)
    if request.method == "GET":
        related_product = Products.objects.filter(status=True, category=product.category)
        reviews = Reviews.objects.select_related('product').filter(product=product.id)
        star = 0
        for rating in reviews:
            star += rating.star.value

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
        stars = []
        star = 0
        for review in reviews:
            star = review.star.value
            stars.append(star)
        if len(stars) > 1:
            simple_star = statistics.mean(stars)
        elif len(stars) == 1:
            simple_star = star
        else:
            simple_star = 0
        if stars:
            star5 = stars.count(5) * 100 / len(stars)
            count5 = stars.count(5)
            star4 = stars.count(4) * 100 / len(stars)
            count4 = stars.count(4)
            star3 = stars.count(3) * 100 / len(stars)
            count3 = stars.count(3)
            star2 = stars.count(2) * 100 / len(stars)
            count2 = stars.count(2)
            star1 = stars.count(1) * 100 / len(stars)
            count1 = stars.count(1)
        else:
            star5 = 0
            count5 = 0
            star4 = 0
            count4 = 0
            star3 = 0
            count3 = 0
            star2 = 0
            count2 = 0
            star1 = 0
            count1 = 0


        context = {
            'star5': star5,
            'count5': count5,
            'star4': star4,
            'count4': count4,
            'star3': star3,
            'count3': count3,
            'star2': star2,
            'count2': count2,
            'star1': star1,
            'count1': count1,
            'product': product,
            'related_product': related_product[:3],
            'reviews': reviews,
            'form': CartAddProductForm,
            'star_form': ReviewsForm,
            'price_with_discount': float(product.price) - (
                        float(product.price) * (product.discount / 100)) if product.discount else 0,
            'page_object': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
            'simple_star': int(simple_star),
            'simple_star1': round(simple_star, 1),
        }

        if star > 0:
            context['rating'] = round(star/len(reviews))
        return render(request, 'product.html', context=context)

    elif request.method == "POST":
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['quantity']
            if data <= 0:
                return redirect('product_detail_url', product.slug)
            cart = Cart(request)
            cart.add(product=product, quantity=form.cleaned_data.get('quantity'),
                     update_quantity=form.cleaned_data.get('update'))
            return redirect('product_detail_url', product.slug)


class AddReview(CreateView):
    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        product = Products.objects.get(id=pk)
        rating = RatingStar.objects.get(value=int(request.POST.get('star')))
        if request.user.is_authenticated:
            if form.is_valid():
                Reviews.objects.create(
                    user=request.user,
                    product=product,
                    text=request.POST.get('text'),
                    star=rating,
                )
            return redirect("product_detail_url", product.slug)
        return redirect("login")


class ReviewsView(DetailView):
    template_name = 'reviews.html'
    model = Products
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ReviewsView, self).get_context_data(**kwargs)
        reviews = Reviews.objects.select_related('product').filter(product=self.object.id)
        context["reviews"] = reviews
        return context


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
        for product in favorites:
            product.price_with_discount = float(product.price) - (
                    float(product.price) * (product.discount / 100)) if product.discount else 0
        for product in favorites:
            reviews = Reviews.objects.select_related('product').filter(product=product.id)
            star = 0
            stars = []
            for review in reviews:
                star = review.star.value
                stars.append(star)
            if len(stars) > 1:
                product.simple_star = statistics.mean(stars)
            elif len(stars) == 1:
                product.simple_star = star
            else:
                product.simple_star = 0
        context = {
            'products': favorites
        }
        return render(request, 'favorites.html', context=context)
    else:
        return redirect('login')


class ProductcategoryListView(ListView):
    template_name = 'store.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self, **kwargs):
        category_slug = self.kwargs.get("category_slug")
        category = get_object_or_404(Categories, slug=category_slug)
        queryset = self.model.objects.filter(status=True, category=category)
        for product in queryset:
            product.price_with_discount = float(product.price) - (
                    float(product.price) * (product.discount / 100)) if product.discount else 0
        for product in queryset:
            reviews = Reviews.objects.select_related('product').filter(product=product.id)
            star = 0
            stars = []
            for review in reviews:
                star = review.star.value
                stars.append(star)
            if len(stars) > 1:
                product.simple_star = statistics.mean(stars)
            elif len(stars) == 1:
                product.simple_star = star
            else:
                product.simple_star = 0
        return queryset







