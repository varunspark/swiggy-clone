from django.db import connection
from django.http import JsonResponse
from rest_framework import generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Restaurant, Order
from .serializers import (RestaurantSerializer, RestaurantDetailSerializer,
                          OrderSerializer, RegisterSerializer)


def health(request):
    """Used by load balancers / Docker HEALTHCHECK / Kubernetes probes."""
    try:
        connection.ensure_connection()
        return JsonResponse({"status": "ok", "db": "up"})
    except Exception:
        return JsonResponse({"status": "error", "db": "down"}, status=503)


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.prefetch_related("menu")

    def get_serializer_class(self):
        return RestaurantDetailSerializer if self.action == "retrieve" else RestaurantSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by("-created_at")


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        return Response({"token": Token.objects.create(user=user).key}, status=201)
