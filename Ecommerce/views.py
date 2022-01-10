from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'Ecommerce/home.html', context)

def product_details(request, id):
    item = Item.objects.get(id=id)
    similar = Item.objects.filter(catigory=item.catigory)
    context = {
        'item': item,
        'items': similar[0:10]
    }
    return render(request, 'Ecommerce/product.html', context)