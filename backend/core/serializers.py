from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "price", "is_veg"]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "cuisine", "rating", "address"]


class RestaurantDetailSerializer(RestaurantSerializer):
    menu = MenuItemSerializer(many=True, read_only=True)

    class Meta(RestaurantSerializer.Meta):
        fields = RestaurantSerializer.Meta.fields + ["menu"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity", "price"]
        read_only_fields = ["price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "restaurant", "status", "total", "created_at", "items"]
        read_only_fields = ["status", "total", "created_at"]

    def create(self, validated):
        items = validated.pop("items")
        order = Order.objects.create(customer=self.context["request"].user, **validated)
        total = 0
        for i in items:
            menu_item = i["menu_item"]
            if menu_item.restaurant_id != order.restaurant_id:
                raise serializers.ValidationError("Item belongs to a different restaurant")
            OrderItem.objects.create(order=order, menu_item=menu_item,
                                     quantity=i["quantity"], price=menu_item.price)
            total += menu_item.price * i["quantity"]
        order.total = total
        order.save()
        return order


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated):
        return User.objects.create_user(**validated)
