from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(ModelSerializer):
    number_of_lessons = SerializerMethodField()

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ("name", "description", "number_of_lessons")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
