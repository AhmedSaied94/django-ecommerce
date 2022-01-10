from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.

class Catigory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Reviews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.CharField(max_length=1)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    img = models.ImageField(upload_to='items/imgs', null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    catigory = models.ForeignKey('Catigory', on_delete=models.CASCADE)
    

    class Meta:
        ordering = ['-added_date']
    
    @property
    def rating(self):
        if not self.Review:
            rating = 'N/A'
        else:
            reviews = self.Review_set.all
            total_rate = 0
            for i in reviews:
                total_rate += int(i.rating)
            rating = str(total_rate / len(reviews))
        return rating
    
    def get_absolute_url(self):
        return reverse('Ecommerce:product-details', kwargs={
            'slug':self.id
        })

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