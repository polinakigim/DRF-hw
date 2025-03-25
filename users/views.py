from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Payment
from users.serializers import PaymentSerializer

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
