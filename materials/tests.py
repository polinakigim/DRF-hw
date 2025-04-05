from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user1@email.com')
        self.course = Course.objects.create(name='Course 1', description='test descriprion')
        self.lesson = Lesson.objects.create(name='Lesson 1', course=self.course, owner=self.user,
                                            link='https://www.youtube.com/watch?v=SOME_ID')
        self.subscription_url = reverse('materials:subscription')
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lessons_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse('materials:lessons_create')
        data = {
            'name': 'Lesson 2',
            'description': 'Описание второго урока',
            'course': self.course.pk,
            'owner': self.user.pk,
            'link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse('materials:lessons_update', args=(self.lesson.pk,))
        data = {
            'name': 'Lesson 3 PATCH',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'Lesson 3 PATCH'
        )

    def test_lesson_delete(self):
        url = reverse('materials:lessons_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.lesson.pk, 'name': self.lesson.name, 'preview': None, 'description': None,
             'link': 'https://www.youtube.com/watch?v=SOME_ID', 'course': self.course.pk, 'owner': self.user.pk}]
                }
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_create_subscription(self):
        data = {"course_id": self.course.pk}
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['message'], "Подписка добавлена"
        )
        self.assertEqual(
            Subscription.objects.filter(user=self.user, course=self.course).count(), 1
        )

    def test_delete_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.assertEqual(
            Subscription.objects.filter(user=self.user, course=self.course).count(), 1
        )
        data = {"course_id": self.course.pk}
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['message'], "Подписка удалена"
        )
        self.assertEqual(
            Subscription.objects.filter(user=self.user, course=self.course).count(), 0
        )

    def test_subscription_requires_authentication(self):
        self.client.logout()
        data = {"course_id": self.course.pk}
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )