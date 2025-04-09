from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Subscription


@shared_task
def send_course_update_mail(course_id):
    """Обновление курса и отправка письма"""

    subscriptions = Subscription.objects.filter(course_id=course_id)
    recipient_emails = subscriptions.values_list("user__email", flat=True)
    if not recipient_emails:
        return

    send_mail(
        "Курс обновлен",
        "Обновления по курсу доступны. Проверьте свои материалы!",
        settings.EMAIL_HOST_USER,
        recipient_emails,
        fail_silently=False,
    )
