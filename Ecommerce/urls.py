from django.urls import path
from .views import *


app_name = 'shopping'

urlpatterns = [
    path('', items_list, name='items-list'),
    path('product/<int:id>', product_details, name='product-details')
]