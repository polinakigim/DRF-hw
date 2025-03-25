from django.urls import path, include
from rest_framework.routers import SimpleRouter
from users.views import PaymentViewSet, PaymentListAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
]
urlpatterns += router.urls
