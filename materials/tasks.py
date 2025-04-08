from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from config import settings
from materials.models import Subscription
from users.models import User


@shared_task
def send_course_update_mail(course_id):
    """Обновление курса и отправка письма"""

    subscriptions = Subscription.objects.filter(course_id=course_id)
    for subscription in subscriptions:
        send_mail(
            'Курс обновлен',
            'Обновления по курсу доступны. Проверьте свои материалы!',
            settings.EMAIL_HOST_USER,
            [subscription.user.email],
            fail_silently=False,
        )


@shared_task
def deactivate_inactive_users():
    """Блокировка пользователей, не заходивших более месяца"""
    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} отключен')
        else:
            print(f'Пользователь {user.email} активен')
