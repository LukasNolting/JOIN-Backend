from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import CustomUser, TaskItem, Contacts


class LoginViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password',
            email='test@example.com'
        )
        self.url = reverse('login')

    def test_login_valid_user(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_login_invalid_user(self):
        response = self.client.post(self.url, {'username': 'wronguser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserCreateViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('user-register')

    def test_create_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'newuser')


class UserGetViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('get_users')
        CustomUser.objects.create_user(
            username='testuser',
            password='password',
            email='test@example.com'
        )

    def test_get_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')


class TaskViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task = TaskItem.objects.create(
            title='Test Task',
            description='Task description'
        )
        self.url = reverse('task-detail', kwargs={'id': self.task.id})

    def test_get_task(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_post_task(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New task description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskItem.objects.count(), 2)

    def test_delete_task(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskItem.objects.count(), 0)

    def test_put_task(self):
        data = {
            'title': 'Updated Task',
            'description': 'Updated description'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskItem.objects.get(id=self.task.id).title, 'Updated Task')


class ContactsViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.contact = Contacts.objects.create(
            name='Test Contact',
            email='contact@example.com'
        )
        self.url = reverse('contact-detail', kwargs={'id': self.contact.id})

    def test_get_contacts(self):
        url = reverse('contact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Contact')

    def test_post_contact(self):
        url = reverse('contact-list')
        data = {
            'name': 'New Contact',
            'email': 'newcontact@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contacts.objects.count(), 2)

    def test_delete_contact(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contacts.objects.count(), 0)

    def test_put_contact(self):
        data = {
            'name': 'Updated Contact',
            'email': 'updatedcontact@example.com'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contacts.objects.get(id=self.contact.id).name, 'Updated Contact')
