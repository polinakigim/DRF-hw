from django.core.management.base import BaseCommand
from django.utils import timezone

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Заполняет таблицу Payment тестовыми данными"

    def handle(self, *args, **kwargs):
        try:
            user_1 = User.objects.first()
            if not user_1:
                user_1 = User.objects.create(
                    email="user1@example.com", password="password123"
                )

            user_2 = User.objects.all()[1] if User.objects.count() > 1 else None
            if not user_2:
                user_2 = User.objects.create(
                    email="user2@example.com", password="password123"
                )

            course_1 = Course.objects.first()
            lesson_1 = Lesson.objects.first()

            if not course_1:
                course_1 = Course.objects.create(
                    name="Курс 1", description="Описание курса 1"
                )
            if not lesson_1:
                lesson_1 = Lesson.objects.create(
                    course=course_1,
                    name="Урок 1",
                    description="Описание урока 1",
                    link="http://lesson1.com",
                )

            Payment.objects.create(
                user=user_1,
                payment_date=timezone.now(),
                paid_course=course_1,
                paid_lesson=lesson_1,
                payment_amount=1000.00,
                payment_method="наличные",
            )

            Payment.objects.create(
                user=user_2,
                payment_date=timezone.now(),
                paid_course=course_1,
                paid_lesson=None,
                payment_amount=500.00,
                payment_method="перевод на счет",
            )

            self.stdout.write(
                self.style.SUCCESS("Данные платежей успешно записаны в таблицу.")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
