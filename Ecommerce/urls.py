from os import name
from django.urls import path
from .views import *


app_name = 'Ecommerce'

urlpatterns = [
    path('', products, name='items-list'),
    path('product/<int:id>/', product_details, name='product-details'),
    path('add-to-card/<int:id>', add_to_card, name='add-to-card'),
    path('remove-from-card/<int:id>/<str:num>', remove_from_card, name='remove-from-card'),
    path('add-to-wishlist/<int:id>/', add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/<int:id>/', remove_from_wishlist, name='remove-from-wishlist'),
    path('wishlist/', wishlist_items, name='wishlist'),
    path('cart/', cart_summury, name='cart'),
    path('checkout/', checkout, name='checkout')
]