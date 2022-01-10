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
    dis_price = models.FloatField(null=True, blank=True)
    img = models.ImageField(upload_to='items/imgs', null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    catigory = models.ForeignKey('Catigory', on_delete=models.CASCADE)
    description = models.TextField()
    


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
            'id':self.id
        })

    def get_add_to_card_url(self):
        return reverse('Ecommerce:add-to-card', kwargs={
            'id':self.id
        })

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isOrderd = models.BooleanField(default=False)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title


class ShopingCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField('OrderItem')
    start_date = models.DateTimeField(auto_now_add=True)
    orderd_date = models.DateTimeField()
    isOrderd = models.BooleanField(default=False)


    class Meta:
        ordering = ['-orderd_date']
    
    def __str__(self):
        return self.user.username