from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import Payment, User, Paying
from users.serializers import PaymentSerializer, UserSerializer, UserRegisterSerializer, PayingSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [SearchFilter, OrderingFilter]

    # Параметры поиска
    search_fields = ['payment_method']  # Можем искать по способу оплаты

    # Параметры для сортировки
    ordering_fields = ['payment_date', 'payment_amount']  # Сортировка по дате оплаты и сумме
    ordering = ['payment_date']  # По умолчанию сортировка по дате оплаты

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по курсу
        course = self.request.query_params.get('paid_course')
        if course:
            queryset = queryset.filter(paid_course__id=course)

        # Фильтрация по уроку
        lesson = self.request.query_params.get('paid_lesson')
        if lesson:
            queryset = queryset.filter(paid_lesson__id=lesson)

        # Фильтрация по способу оплаты
        payment_method = self.request.query_params.get('payment_method')
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        return queryset

class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

class PaymentRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

class PaymentUpdateAPIView(UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

class PaymentDestroyAPIView(DestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class PayingCreateAPIView(CreateAPIView):
    queryset = Paying.objects.all()
    serializer_class = PayingSerializer

    def perform_create(self, serializer):
        pay = serializer.save(user=self.request.user)
        stripe_product_id = create_stripe_product(pay)
        price = create_stripe_price(stripe_product_id, pay)
        session_id, payment_link = create_stripe_session(price)
        pay.session_id = session_id
        pay.link = payment_link
        pay.save()