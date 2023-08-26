from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user
        self.user = User.objects.create_user(
            username='demouser',
            password='demopwd'
        )

        # Create a post
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post',
            content='Test content',
            owner=self.user
        )

    def test_get_post_list(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Post',
            'description': 'This is a new post',
            'content': 'New content',
            'owner': self.user.id
        }
        response = self.client.post('/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_detail(self):
        response = self.client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Post'}
        response = self.client.put(f'/posts/{self.post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post')

    def test_delete_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
