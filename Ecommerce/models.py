from django.db import models
from django.conf import settings

# Create your models here.

class Catigory(models.Model):
    name = models.CharField(max_length=100)

class Label(models.Model):
    name = models.CharField(max_length=100)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    img = models.ImageField(upload_to='items/imgs', null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    catigory = models.ForeignKey('Catigory', on_delete=models.CASCADE)
    label = models.ForeignKey('Label', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title


class ShopingCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField('OrderItem')
    start_date = models.DateTimeField(auto_now_add=True)
    orderd_date = models.DateTimeField()

    class Meta:
        ordering = ['-orderd_date']
    
    def __str__(self):
        return self.user.username