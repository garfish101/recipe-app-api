from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Tests creating a user with email in succesfull"""
        email = 'testemail@me.com'
        password = 'core24299'

        user = get_user_model().objects.create_user(
            email = email,
            password=password 
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password,password)

    def test_new_user_email_normalize(self):
        """tests if user email is normalized""" 
        email = 'testemail@mWEBe.com'
        password = 'core24299'
        user = get_user_model().objects.create_user(
            email = email,)
            

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
            '''test for emails when user email is invalid'''
            with self.assertRaises(ValueError):
                get_user_model().objects.create_user(None,'test123')
    
    def test_create_new_superuser(self):
        """tests if create super user if working"""
        user = get_user_model().objects.create_superuser(
            "testing@me.com",
            "pasword123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    