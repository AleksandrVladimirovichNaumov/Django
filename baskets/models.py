from django.db import models
from users.models import User
from products.models import Product
# Create your models here.

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина {self.user.name} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    @staticmethod
    def total_sum(user):
        baskets=Basket.objects.filter(user=user)
        return sum(basket.sum() for basket in baskets)

    @staticmethod
    def total_quantity(user):
        baskets=Basket.objects.filter(user=user)
        return sum(basket.quantity for basket in baskets)


    def total_sum_qnty(request):
        total_sum = 0
        total_qnty = 0
        for basket in Basket.objects.filter(user=request.user):
            total_sum += basket.sum()
            total_qnty += basket.quantity
        return total_sum, total_qnty
