from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from baskets.models import Basket
from geekshop import settings
from products.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'
    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлен'),
        (PAID, 'оплачено'),
        (PROCEEDED, 'формируется'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'заказ отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус', max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def get_total_quantity(self):
        items = self.order_item.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.order_item.select_related()
        print(items)
        print(sum(list(map(lambda x: x.get_product_cost() *x.quantity, items))))
        return sum(list(map(lambda x: x.get_product_cost()* x.quantity, items)))

    def get_items(self):
        pass

    def ge_summary(self):
        items=self.order_item.select_related()
        return {
            'get_total_cost': sum(list(map(lambda x: x.get_product_cost()* x.quantity, items))),
            'get_total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def delete(self, using=None, keep_parents=False):
        for item in self.order_item.select_related():
            item.product.quantity += item.quantity
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='order_item', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk).quantity


# @receiver(pre_delete, sender=Basket)
# @receiver(pre_delete, sender=OrderItem)
# def product_quantity_update_delete(sender, instance, **kwargs):
#     instance.product.quantity += instance.quantity
#     instance.product.save()
#
# @receiver(pre_save, sender=Basket)
# @receiver(pre_save, sender=OrderItem)
# def product_quantity_update_save(sender, instance, **kwargs):
#     if instance.pk:
#         instance.product.quantity -= instance.quantity - instance.get_item(int(instance.pk))
#     else:
#         instance.product.quantity -= instance.quantity
#     instance.product.save()
