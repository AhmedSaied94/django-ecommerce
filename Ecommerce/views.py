from distutils import log
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
# Create your views here.

def products(request):
    context = {
        'items': Item.objects.all(),
        'user':request.user
    }
    return render(request, 'Ecommerce/home.html', context)

def product_details(request, id):
    item = Item.objects.get(id=id)
    try:
        wishlist_exist = request.user.wishlist_set.first().items.filter(id=id).exists()
    except:
        wishlist_exist = False
    similar = Item.objects.filter(catigory=item.catigory)
    context = {
        'item': item,
        'items': similar[0:10],
        'user':request.user,
        'range':range(5),
        'wishlist_exist':wishlist_exist
    }
    print(item.rating)
    return render(request, 'Ecommerce/product.html', context)

@login_required
def add_to_card(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        isOrderd=False
    )
    order_date = timezone.now()
    cur_order = ShopingCard.objects.filter(user=request.user, isOrderd=False)
    if cur_order.exists():
        order = cur_order.first()
        if order.items.filter(item__id=item.id).exists():
            order_item.qty += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = ShopingCard.objects.create(user=request.user, orderd_date=order_date)
        order.items.add(order_item)
    return redirect(request.META['HTTP_REFERER'], id=id)
            

def remove_from_card(request, id, num):
    item = get_object_or_404(Item, id=id)
    order_item = OrderItem.objects.get(
        item=item,
        user=request.user,
        isOrderd=False
    )
    cur_order = ShopingCard.objects.filter(user=request.user, isOrderd=False)
    order = cur_order[0]
    if num == 'one':
        if order_item.qty > 1:
            order_item.qty -= 1
            order_item.save()
        else:
            order.items.remove(order_item)
            order_item.delete()
    else:
        order.items.remove(order_item)
        order_item.delete()
    print(request.path_info)
    return redirect(request.META['HTTP_REFERER'], id=id)

@login_required
def add_to_wishlist(request, id):
    item = get_object_or_404(Item, id=id)
    cur_wishlist = WishList.objects.filter(user=request.user)
    if cur_wishlist.exists():
        wishlist = cur_wishlist[0]
    else:
        wishlist = WishList.objects.create(user= request.user,)
    wishlist.items.add(item)    
    return redirect(request.META['HTTP_REFERER'], id=id)

def remove_from_wishlist(request, id):
    item = get_object_or_404(Item, id=id)
    cur_wishlist = WishList.objects.filter(user=request.user)
    if cur_wishlist.exists:
        wishlist= cur_wishlist[0]
        wishlist.items.remove(item)
        return redirect(request.META['HTTP_REFERER'], id=id)

@login_required
def wishlist_items(request):
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    try:
        items = wishlist.items.all()
    except:
        items = False
    context = {
        'items':items,
        'user':request.user
    }
    return render(request, 'Ecommerce/wishlist.html', context)

@login_required
def cart_summury(request):

    qs = ShopingCard.objects.filter(user=request.user, isOrderd=False)
    if qs.exists():
        order = qs[0]
        context = {
            'cart':order
        }
    else:
        context = {
            'cart':False
        }
    return render(request, 'Ecommerce/cart.html', context)


@login_required
def checkout(request):
    form = CheckoutForm()
    if request.method == 'POST':
        form = CheckoutForm(data=request.POST)
        order = OrderItem.objects.filter(user=request.user, isOrderd=False)
        if order.exists():
            if form.is_valid():
                data = form.cleaned_data
                billing_address = BillingAddress(
                    user = request.user,
                    address = data['address'],
                    city = data['city'],
                    country = data['country'],
                    zip = data['zip'],
                    telephone = data['telephone'],
                    notes = data['notes']
                )
                billing_address.save()
                order[0].billing_address = billing_address
                order['0'].save()
                return redirect('Ecommerce:checkout')
        return redirect('Ecommerce:cart')
    return render(request, 'Ecommerce/checkout.html', context={'form':form})
    
