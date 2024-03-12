from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)


class Payment(models.Model):
    number = models.IntegerField(blank=True, null=True)
    status = models.BooleanField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'customer'})

    def __str__(self):
        return str(self.number)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def calculate_price(self):
        return (self.product.price - self.product.discount) * self.quantity
