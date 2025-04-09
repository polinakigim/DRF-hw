from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import LinkToVideoValidator


class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(), many=True
    )  # Простой список ID уроков
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkToVideoValidator(field="link")]


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, lesson):
        return Lesson.objects.filter.count(course=lesson.course)

    class Meta:
        model = Course
        fields = ("name", "description", "lessons_count")
