from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import RestaurantViewSet, OrderViewSet, RegisterView

router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", obtain_auth_token),
    path("", include(router.urls)),
]
