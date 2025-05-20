from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PayingCreateAPIView, PaymentListAPIView,
                         PaymentViewSet, UserRegisterView, UserViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"payments", PaymentViewSet)
router.register(r"users", UserViewSet)


urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("paying/", PayingCreateAPIView.as_view(), name="paying"),
]
urlpatterns += router.urls
