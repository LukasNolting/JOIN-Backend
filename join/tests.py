from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import CustomUser, TaskItem, Contacts

# Documentation for the test cases

# This file contains a suite of automated tests for the API views of the Django application.
# It tests functionalities related to user authentication, user creation,
# task management, and contact management, ensuring the API behaves as expected.

class LoginViewTests(APITestCase):
    """Tests for the login functionality of users."""

    def setUp(self):
        """Sets up a test user and the login URL."""
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password',
            email='test@example.com'
        )
        self.url = reverse('login')

    def test_login_valid_user(self):
        """Tests login with valid credentials."""
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_login_invalid_user(self):
        """Tests login with invalid credentials."""
        response = self.client.post(self.url, {'username': 'wronguser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserCreateViewTests(APITestCase):
    """Tests for the user registration endpoint."""

    def setUp(self):
        """Sets up the user registration URL."""
        self.url = reverse('user-register')

    def test_create_user(self):
        """Tests the creation of a new user."""
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
    """Tests for retrieving user data."""

    def setUp(self):
        """Sets up a test user and the URL for getting users."""
        self.url = reverse('get_users')
        CustomUser.objects.create_user(
            username='testuser',
            password='password',
            email='test@example.com'
        )

    def test_get_users(self):
        """Tests the retrieval of user data."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')


class TaskViewTests(APITestCase):
    """Tests for task management functionalities."""

    def setUp(self):
        """Sets up a test task and the URL for task detail."""
        self.client = APIClient()
        self.task = TaskItem.objects.create(
            title='Test Task',
            description='Task description'
        )
        self.url = reverse('task-detail', kwargs={'id': self.task.id})

    def test_get_task(self):
        """Tests the retrieval of a specific task."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_post_task(self):
        """Tests the creation of a new task."""
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New task description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskItem.objects.count(), 2)

    def test_delete_task(self):
        """Tests the deletion of a task."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskItem.objects.count(), 0)

    def test_put_task(self):
        """Tests updating an existing task."""
        data = {
            'title': 'Updated Task',
            'description': 'Updated description'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskItem.objects.get(id=self.task.id).title, 'Updated Task')


class ContactsViewTests(APITestCase):
    """Tests for contacts management functionalities."""

    def setUp(self):
        """Sets up a test contact and the URL for contact detail."""
        self.client = APIClient()
        self.contact = Contacts.objects.create(
            name='Test Contact',
            email='contact@example.com'
        )
        self.url = reverse('contact-detail', kwargs={'id': self.contact.id})

    def test_get_contacts(self):
        """Tests the retrieval of contact data."""
        url = reverse('contact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Contact')

    def test_post_contact(self):
        """Tests the creation of a new contact."""
        url = reverse('contact-list')
        data = {
            'name': 'New Contact',
            'email': 'newcontact@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contacts.objects.count(), 2)

    def test_delete_contact(self):
        """Tests the deletion of a contact."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contacts.objects.count(), 0)

    def test_put_contact(self):
        """Tests updating an existing contact."""
        data = {
            'name': 'Updated Contact',
            'email': 'updatedcontact@example.com'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contacts.objects.get(id=self.contact.id).name, 'Updated Contact')
