# chat/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ChatRoom
from django.contrib.auth.models import User

class ChatRoomViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)  # Authenticate the client
        self.chatroom1 = ChatRoom.objects.create(name='Room 1', is_group_chat=True)
        self.chatroom2 = ChatRoom.objects.create(name='Room 2', is_group_chat=False)
        self.chatroom1.users.add(self.user)
        self.chatroom2.users.add(self.user)

    def test_list_chatrooms(self):
        response = self.client.get('/chatrooms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Check for paginated results

        # Check for specific chatroom names in the response
        names = [item['name'] for item in response.data['results']]
        self.assertIn('Room 1', names)
        self.assertIn('Room 2', names)

    def test_create_chatroom(self):
        data = {'name': 'New Room', 'is_group_chat': True}
        response = self.client.post('/chatrooms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 3)  # Check that a new chatroom was created
        self.assertEqual(ChatRoom.objects.last().name, 'New Room')

    def test_create_chatroom_invalid_data(self):
        data = {'name': '', 'is_group_chat': True} #empty name
        response = self.client.post('/chatrooms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ChatRoom.objects.count(), 2) #chatroom count should not change.

    def test_create_chatroom_missing_is_group_chat(self):
        data = {'name': 'Missing is_group_chat'}
        response = self.client.post('/chatrooms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ChatRoom.objects.count(), 2)

    def test_create_chatroom_missing_name(self):
        data = {'is_group_chat': True}
        response = self.client.post('/chatrooms/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ChatRoom.objects.count(), 2)