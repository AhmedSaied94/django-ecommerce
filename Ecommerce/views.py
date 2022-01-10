from django.shortcuts import get_object_or_404, render, redirect
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

def add_to_card(request, id):
    item = get_object_or_404(Item, id=id)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        isOrderd=False
    )
    cur_order = ShopingCard.objects.filter(user=request.user, isOrderd=False)
    if cur_order.exists():
        order = cur_order
        if order.items.filter(item__id=item.id).exists():
            order_item.qty += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = ShopingCard.objects.create(user=request.user)
        order.items.add(order_item)
    return redirect('Ecommerce:product_details', id=id)
            
