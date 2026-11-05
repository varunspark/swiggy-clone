from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=120)
    cuisine = models.CharField(max_length=80)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="menu", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_veg = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = "PLACED"
        ACCEPTED = "ACCEPTED"
        PREPARING = "PREPARING"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
        DELIVERED = "DELIVERED"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)
