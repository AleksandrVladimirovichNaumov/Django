from django.db import models
from django.utils.functional import cached_property

from users.models import User
from products.models import Product


# Create your models here.


class BasketQueryset(models.QuerySet):

    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity +=item.quantity
            item.product.save()
        super(BasketQueryset, self).delete()


class Basket(models.Model):
    objects = BasketQueryset.as_manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    # @staticmethod
    # def total_sum(self):
    #     baskets=Basket.objects.filter(user=self.user)
    #     return sum(basket.sum() for basket in baskets)
    #
    # @staticmethod
    # def total_quantity(self):
    #     baskets=Basket.objects.filter(self.user)
    #     return sum(basket.quantity for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        # baskets = self.get_cache_item
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        # baskets = self.get_cache_item
        return sum(basket.sum() for basket in baskets)

    # def total_sum_qnty(request):
    #     total_sum = 0
    #     total_qnty = 0
    #     for basket in Basket.objects.filter(user=request.user):
    #         total_sum += basket.sum()
    #         total_qnty += basket.quantity
    #     return total_sum, total_qnty

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()
        super(Basket, self).delete()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            self.product.quantity -= self.quantity - self.get_item(int(self.pk))
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(Basket, self).save()

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity

    @cached_property
    def get_cache_item(self):
        return self.user.basket.select_related()
