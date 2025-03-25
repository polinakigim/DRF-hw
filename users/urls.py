from django.urls import path, include
from rest_framework.routers import SimpleRouter
from users.views import PaymentViewSet, PaymentListAPIView, UserViewSet, UserRegisterView
from users.apps import UsersConfig
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),

    path('register/', UserRegisterView.as_view(), name='register'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += router.urls
