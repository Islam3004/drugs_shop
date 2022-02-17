from .models import Categories

def get_category(request):
    category = Categories.objects.all()
    context = {"categories":category}
    return context