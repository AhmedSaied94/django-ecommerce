from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def items_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'Ecommerce/items-list.html', context)