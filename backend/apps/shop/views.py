from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Products, Reviews, Categories
from .forms import ReviewsForm
# Create your views here.

class ProductListView(ListView):
    template_name = 'store.html'
    queryset = Products.objects.filter(status=True)
    context_object_name = 'products'
    paginate_by = 10


class ProductDetailView(DetailView):
    template_name = 'product.html'
    model = Products
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        related_product = Products.ogject.filter(status=True, category=self.object.category)
        context['related_product'] = related_product
        return context

    
    


