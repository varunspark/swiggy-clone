from django.contrib import admin
from .models import Restaurant, MenuItem, Order, OrderItem

admin.site.register([Restaurant, MenuItem, Order, OrderItem])
