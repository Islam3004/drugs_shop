
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, CreateView
from .models import Products, Reviews, Categories, RatingStar
from .forms import ReviewsForm
from backend.apps.cart.forms import CartAddProductForm
from backend.apps.cart.cart import Cart
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404

# Create your views here.



class HomeView(ListView):
    template_name = 'index.html'
    queryset = Products.objects.filter(status=True)


class ProductListView(ListView):
    template_name = 'store.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self, **kwargs):
        search_query = self.request.GET.get("q", '')
        if search_query:
            queryset = self.model.objects.filter(title__icontains=self.request.GET.get("q", ''))
            return queryset
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            category = get_object_or_404(Categories, slug=category_slug)
            queryset = self.model.objects.filter(status=True, category=category)
            return queryset
        price_min_query = self.request.GET.get("min", "")
        if price_min_query:
            queryset = self.model.objects.filter(quantity__icontains=self.request.GET.get("min",''))
            return queryset
        queryset = self.model.objects.filter(status=True)
        return queryset

    
class ProductDetailView(FormMixin, DetailView):
    template_name = 'product.html'
    model = Products
    context_object_name = 'product'
    form_class = CartAddProductForm


    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        related_product = Products.objects.filter(status=True, category=self.object.category)
        reviews = Reviews.objects.select_related('product').filter(product=self.object.id)
        reviews_stars = Reviews.objects.filter()
        context['related_product'] = related_product[:4] if len(related_product) > 4 else related_product
        context["star_form"] = ReviewsForm
        context["reviews"] = reviews[:3] if len(reviews) > 3 else reviews
        return context


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
            return redirect(f"/product/{product.id}/")
        return redirect("/registration/login")




class ReviewsView(DetailView):
    template_name = 'reviews.html'
    model = Products
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context = super(ReviewsView, self).get_context_data(**kwargs)
        reviews = Reviews.objects.select_related('product').filter(product=self.object.id)
        context["reviews"] = reviews
        return context

#




