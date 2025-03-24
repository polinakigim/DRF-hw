from rest_framework import serializers
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'city', 'avatar']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'payment_amount', 'payment_method']


class PaymentDetailSerializer(PaymentSerializer):
    paid_course_name = serializers.CharField(source='paid_course.name', read_only=True)
    paid_lesson_name = serializers.CharField(source='paid_lesson.name', read_only=True)

    class Meta(PaymentSerializer.Meta):
        fields = PaymentSerializer.Meta.fields + ['paid_course_name', 'paid_lesson_name']
