import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Topic

class TopicResourceTests(APITestCase):
    topics = [{
                'name': 'Business',
                'description': ''
            },
            {
                'name': 'Energy',
                'description': ''
            }]

    def setUp(self):
        self.admin_user = User.objects.create_user(
            'guido', 'guido@foo.ie', 'foo', is_staff=True, is_superuser=True
        )

        url = reverse('api-token-auth')
        response = self.client.post(
            url, {'username': 'guido', 'password': 'foo'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'The token should be successfully returned.')

        response_content = json.loads(response.content.decode('utf-8'))
        self.token = response_content['token']
        self.header = {'HTTP_AUTHORIZATION': 'JWT {}'.format(self.token)}

    def test_create_topic(self):
        """
        Ensure we can create a new topic object.
        """
        url = reverse('topic-list')
        data = {'name': 'Topic Name'}
        response = self.client.post(url, data, format='json', **self.header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Topic.objects.get().name, 'Topic Name')

    def test_edit_profile(self):
        user = User.objects.create_user('enmanuel', '', 'foo')
        user.save()
        url = reverse('user-detail', args=[user.id])
        self.client.get(url, format='json', **self.header)

        url = reverse('profile-detail', args=[user.id])
        data = {
            # 'full_name': 'Yaima Acosta Hernandez',
            'first_name': 'Enmanuel',
            'last_name': 'Garcia',
            'email': 'guidoenmanuel@gmail.com',
            'current_position': 'Junior Software Engineer',
            'about_you': 'Love watching cartoons',
            'favorite_topics': []
        }

        response = self.client.put(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url, format='json', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('user-detail', args=[user.id])
        response = self.client.get(url, format='json', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'enmanuel')
        self.assertEqual(response.data['first_name'], 'Enmanuel')
        self.assertEqual(response.data['last_name'], 'Garcia')
        self.assertEqual(
            response.data['profile']['current_position'],
            'Junior Software Engineer'
        )
        self.assertEqual(
            response.data['profile']['about_you'],
            'Love watching cartoons'
        )
        self.assertEqual(response.data['email'], 'guidoenmanuel@gmail.com')

    def test_create_topics(self):
        url = reverse('topic-list')
        for topic_data in TopicResourceTests.topics:
            response = self.client.post(url, topic_data, format='json',
                                        **self.header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # retrieve topics
        response = self.client.get(url, format='json', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        topics = json.loads(response.content)
        self.assertEqual(len(topics), 2, 'There should be 2 topics')
        self.assertEqual(topics[0]['name'],
                         TopicResourceTests.topics[0]['name'])

    def test_edit_profile_topics(self):
        user = User.objects.create_user('enmanuel', '', 'foo')
        user.save()
        url = reverse('user-detail', args=[user.id])
        response = self.client.get(url, format='json', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create two topics
        url = reverse('topic-list')
        for topic_data in TopicResourceTests.topics:
            response = self.client.post(url, topic_data, format='json',
                                        **self.header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # retrieve topics
        response = self.client.get(url, format='json', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        topics = json.loads(response.content)
        self.assertEqual(len(topics), 2, 'There should be 2 topics')
        self.assertEqual(topics[0]['name'],
                         TopicResourceTests.topics[0]['name'])

        # Add topics to the user profile
        url = reverse('profile-detail', args=[user.id])
        data = {
            # 'full_name': 'Yaima Acosta Hernandez',
            'first_name': 'Enmanuel',
            'last_name': 'Garcia',
            'email': 'guidoenmanuel@gmail.com',
            'current_position': 'Junior Software Engineer',
            'about_you': 'Love watching cartoons',
            'favorite_topics': map(lambda x: x['url'], topics)
        }
        response = self.client.put(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
