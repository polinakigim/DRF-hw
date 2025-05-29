from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создает нового пользователя с данными, введенными через командную строку"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email пользователя")

    def handle(self, *args, **options):

        email = options["email"]

        try:

            user = User(
                email=email,
            )

            user.set_password(
                "123"
            )  # Здесь можно задать пароль или сделать его динамическим
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Пользователь с email {email} успешно создан!")
            )

        except ValidationError as e:
            self.stderr.write(self.style.ERROR(f"Ошибка валидации: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Произошла ошибка: {e}"))
