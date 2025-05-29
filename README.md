# Домашняя работа по DRF

---

## Описание проекта:

**Django REST Framework-проект с поддержкой Docker, Celery и PostgreSQL.**

## Установка и запуск проекта

### Локально (без Docker)

1. Клонируйте репозиторий:

```bash
git clone <your-repo-url>
cd <your-project-folder>

```

2. Создайте виртуальное окружение и активируйте его:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Примените миграции и запустите сервер:

```bash
python manage.py migrate
python manage.py runserver
```
---

### Запуск через Docker

1. Создайте файл `.env` в корне проекта и добавьте туда переменные окружения (например, как в локальной версии).

2. Запустите контейнеры:

```bash
docker compose up --build -d
```

3. Проект будет доступен по адресу:  
   http://localhost:8000

---

## Деплой на удалённый сервер

Настроено автоматическое развертывание через GitHub Actions.

### Инструкция:

1. Зарегистрируйтесь на [Docker Hub](https://hub.docker.com/)
2. Создайте Personal Access Token:
   - Перейдите в "Account Settings" → "Security"
   - Нажмите "New Access Token", укажите описание, сохраните
3. В репозитории на GitHub:
   - Перейдите в Settings → Secrets → Actions
   - Добавьте:
     - `DOCKER_HUB_USERNAME`
     - `DOCKER_HUB_ACCESS_TOKEN`

4. Запушьте изменения в ветку — GitHub Actions соберёт и отправит Docker-образ в Docker Hub.

---

## Структура проекта

- `docker-compose.yml` — описание контейнеров
- `Dockerfile` — инструкция сборки образа Django-приложения
- `config/` — конфигурация проекта
- `core/` — основное приложение (Courses, Lessons и т.п.)

---

## Тестирование

```bash
python manage.py test
```

