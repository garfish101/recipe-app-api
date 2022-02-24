from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient 
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    """tes"""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users API (PUBLIC)"""
    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """tests creating user with a valid payload is succesfull"""
        payload ={
            'email': 'test@londonappdev.com',
            'password': 'test123',
            'name': 'TestName',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Tests creating user that already exits"""
        payload ={
            'email': 'test@londonappdev.com',
            'password': 'test123',
            'name': 'TestName',}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    def test_password_too_short(self):
        """test that password is more than 5 characters"""
        payload ={
            'email': 'test@londonappdev.com',
            'password': 'ps',
            'name': 'TestName',}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exits = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exits)

    def test_create_token_for_user(self):
        """Test that a token is created for a user"""
        payload ={
            'email': 'test@londonappdev.com',
            'password': 'password123',
            'name': 'TestName',}
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''test that token is not created if invalid credentials are given'''
        create_user(email = 'teste@email.com', password="testpass", name="testename")
        payload = {'email': 'teste@email.com',"password": 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST )
    def test_create_Token_no_user(self):
        """test if token is created if user dosnt exits"""
        payload = {'email': 'teste@email.com',"password": 'password123'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email':'one','password': ''})
        self.assertNotIn('token', res.data )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



