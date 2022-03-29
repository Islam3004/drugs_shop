from django.shortcuts import render, redirect
from backend.apps.cart.models import Order, OrderItem
from django.views.generic import ListView, DetailView, View, CreateView, TemplateView


# Create your views here.


# Create your views here.
    
def order_list_view(request):
    if request.user.is_staff:
        orders = Order.objects.filter(status=False)
        context = {'orders': orders}
        return render(request, 'orders.html', context=context)
    else:
        return redirect('products_list_url')

def sent_order(request, id):
    order = Order.objects.get(id=id)
    order.status = True
    order.save()
    return redirect('order_list_url')

class OrderDetailView(DetailView):
    template_name = 'order_detail.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orderitems = OrderItem.objects.filter(order=self.get_object())
        context["orderitems"] = orderitems
        return context

