from os import name
from django.urls import path
from .views import *


app_name = 'Ecommerce'

urlpatterns = [
    path('', products, name='items-list'),
    path('product/<int:id>/', product_details, name='product-details'),
    path('add-to-card/<int:id>', add_to_card, name='add-to-card'),
]