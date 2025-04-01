from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="course/preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью курса",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name='lessons')
    name = models.CharField(max_length=100, verbose_name="Название урока")
    preview = models.ImageField(
        upload_to="lesson/preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью урока",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    link = models.URLField(max_length=150, verbose_name="Ссылка на урок")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
