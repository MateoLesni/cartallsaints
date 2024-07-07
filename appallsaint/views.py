from django.shortcuts import render
from .models import MenuItem


def menu_view(request):
    items = MenuItem.objects.all()

    # Agrupar los items por categoría
    categories = {}
    for item in items:
        if item.categories not in categories:
            categories[item.categories] = []
        categories[item.categories].append({
            'name': item.name,
            'description': item.description,
            'price': item.price,
        })

    return render(request, 'menu.html', {'categories': categories})