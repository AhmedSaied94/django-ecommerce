from pyexpat import model
from django.db import models
from django.conf import settings
from django.urls import reverse
from django import template
from django_countries.fields import CountryField


class Catigory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Reviews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    dis_price = models.FloatField(null=True, blank=True)
    img = models.ImageField(upload_to='items/imgs', null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    catigory = models.ForeignKey('Catigory', on_delete=models.CASCADE)
    description = models.TextField()
    


    class Meta:
        ordering = ['-added_date']
    
    @property
    def rating(self):
        if self.reviews_set.all().count() <= 0:
            rating = 'N/A'
        else:
            reviews = self.reviews_set.all()
            total_rate = 0
            for i in reviews:
                total_rate += int(i.rating)
            rating = total_rate / len(reviews)
        return rating
    
    def get_absolute_url(self):
        return reverse('Ecommerce:product-details', kwargs={
            'id':self.id
        })

    def get_add_to_card_url(self):
        return reverse('Ecommerce:add-to-card', kwargs={
            'id':self.id
        })

    def get_remove_url_all(self):
        return reverse('Ecommerce:remove-from-card', kwargs={'id':self.id, 'num':'all'})

    def get_remove_url_one(self):
        return reverse('Ecommerce:remove-from-card', kwargs={'id':self.id, 'num':'one'})

    def get_add_to_wishlist_url(self):
        return reverse('Ecommerce:add-to-wishlist', kwargs={'id':self.id})

    def get_remove_from_wishlist_url(self):
        return reverse('Ecommerce:remove-from-wishlist', kwargs={'id':self.id})

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isOrderd = models.BooleanField(default=False)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.qty} of {self.item.title}"

    def get_item_total_price(self):
        if self.item.dis_price:
            total = self.qty * self.item.dis_price
        else:
            total = self.qty * self.item.price
        return total





class ShopingCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField('OrderItem')
    start_date = models.DateTimeField(auto_now_add=True)
    orderd_date = models.DateTimeField()
    isOrderd = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        ordering = ['-orderd_date']
    
    def __str__(self):
        return self.user.username

    def get_total_cart_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_item_total_price()
        return total

class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField('Item')

    def __str__(self):
        return self.Item.title


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=20)
    telephone = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
