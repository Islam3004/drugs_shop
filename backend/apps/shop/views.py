from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Products, Reviews, Categories
from .forms import ReviewsForm
# Create your views here.
from .models import Products
from django.shortcuts import get_object_or_404



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
        context['related_product'] = related_product[:4] if len(related_product) > 4 else related_product
        return context



    


