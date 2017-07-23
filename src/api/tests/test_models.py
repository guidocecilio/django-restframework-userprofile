from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Topic


class TopicResourceTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new topic object.
        """
        url = reverse('topic-list')
        data = {'name': 'Topic Name'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Topic.objects.get().name, 'Topic Name')