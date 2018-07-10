# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License


import sys
from io import StringIO
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.management import call_command
from rest_framework.test import APITestCase
from rest_framework import status
from wger.core.models import UserProfile


class CreateUserTestCase(APITestCase):

    def setUp(self):
        self.user = User(
            username='test_user',
            first_name='test',
            last_name='user',
            email='test@user.com'
        )
        self.user.set_password('secret')
        self.user.save()
        self.client.login(
            username='test_user',
            password='secret'
        )
        self.user.userprofile.can_create_users_via_api = True
        self.user.userprofile.save()
        self.url = reverse('create-user-list')

        self.data = {
            "username": "myuser",
            "first_name": "test",
            "last_name": "user",
            "email": "test@example.com",
            "password": "test_pass"
        }

    def tearDown(self):
        # self.client.logout()
        pass

    def test_create_user_via_rest_api(self):
        '''
        Test that an authorized user can create new users via an API request
        '''

        count_before = User.objects.all().count()
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        count_after = User.objects.all().count()
        self.assertEqual(count_before + 1, count_after)

    def test_can_get_created_users(self):
        '''
        Test that a user can get the users they created via API
        '''

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user(self):
        '''
        Test that an unauthorized user cannot create new users via API
        '''

        self.user.userprofile.can_create_users_via_api = False
        self.user.userprofile.save()
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_creation_command(self):
        '''
        Test the management command for allowing or disallowing the
        creation of new users
        '''

        user = UserProfile.objects.get(user__username='test_user')
        # disallow user
        call_command('allow_user_creation', *['test_user'], **{'disallow': True})
        user.refresh_from_db()
        self.assertFalse(user.can_create_users_via_api)
        # allow user
        call_command('allow_user_creation', *['test_user'], **{'allow': True})
        user.refresh_from_db()
        self.assertTrue(user.can_create_users_via_api)

    def test_list_rest_api_users(self):
        '''
        Test the command for listing users created via API
        '''

        # add a user
        expected = 'Username: {} Email: {} Created by: {}'.format(
                self.data['username'],
                self.data['email'],
                self.user.username
        )
        saved_stdout = sys.stdout
        try:
            self.client.post(self.url, data=self.data)
            out = StringIO()
            sys.stdout = out
            call_command('list_rest_api_users')
            actual = out.getvalue().strip()
            self.assertEqual(expected, actual)
        finally:
            sys.stdout = saved_stdout
