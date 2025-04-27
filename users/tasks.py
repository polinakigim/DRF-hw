from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_inactive_users():
    """Блокировка пользователей, не заходивших более месяца"""
    month_ago = timezone.now() - relativedelta(months=1)
    qs = User.objects.filter(last_login__lte=month_ago, is_active=True)
    qs.update(is_active=False)
