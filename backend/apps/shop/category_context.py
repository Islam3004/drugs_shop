from .models import Categories, Products

def get_category(request):
    category = Categories.objects.all()
    context = {"categories":category}
    return context

