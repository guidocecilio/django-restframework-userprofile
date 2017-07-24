import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from api.models import Topic


class TopicResourceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'guido', 'guido@foo.ie', 'foo', is_staff=True, is_superuser=True
        )


    def test_create_account(self):
        """
        Ensure we can create a new topic object.
        """
        url = reverse('api-token-auth')
        response = self.client.post(
            url, {'username': 'guido', 'password': 'foo'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'The token should be successfully returned.')

        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        url = reverse('topic-list')
        data = {'name': 'Topic Name'}
        header = {'HTTP_AUTHORIZATION': 'JWT {}'.format(token)}
        response = self.client.post(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Topic.objects.get().name, 'Topic Name')