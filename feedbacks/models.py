from django.db import models

# Create your models here.
from products.models import Product
from users.models import User


class Feedback(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    message = models.CharField(max_length=250)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)

