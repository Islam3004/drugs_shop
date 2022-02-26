from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Products, Reviews, Categories, RatingStar
from .forms import ReviewsForm
# Create your views here.
from .models import Products
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse


class HomeView(ListView):
    template_name = 'index.html'
    queryset = Products.objects.filter(status=True)



class ProductListView(ListView):
    template_name = 'store.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        category_slug = self.kwargs.get("category_slug")
        if category_slug is not None:
            category = get_object_or_404(Categories, slug=category_slug)
            queryset = self.model.objects.filter(status=True, category=category)
            return queryset
        queryset = self.model.objects.filter(status=True)
        return queryset

class ProductDetailView(DetailView):
    template_name = 'product.html'
    model = Products
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        related_product = Products.objects.filter(status=True, category=self.object.category)
        reviews = Reviews.objects.select_related('product').filter(product=self.object.id)
        context['related_product'] = related_product[:4] if len(related_product) > 4 else related_product
        context["star_form"] = ReviewsForm
        context["reviews"] = reviews[:3] if len(reviews) > 3 else reviews
        return context


class AddReview(View):

    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        product = Products.objects.get(id=pk)
        rating = RatingStar.objects.get(value=int(request.POST.get('star')))
        if form.is_valid():
            Reviews.objects.create(
                email=request.POST.get('email'),
                name=request.POST.get('name'),
                product=product,
                text=request.POST.get('text'),
                star=rating
            )
        return redirect(f"/product/{product.id}/")



class ReviewsView(DetailView):
    template_name = 'reviews.html'
    model = Products
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ReviewsView, self).get_context_data(**kwargs)
        reviews = Reviews.objects.select_related('product').filter(product=self.object.id)
        context["reviews"] = reviews
        return context






    


