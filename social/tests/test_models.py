import pytest
from django import urls
from django.contrib.auth import get_user_model

from django.test import SimpleTestCase, TestCase

from members.models import User
from social.models import Post, PostTest

'''
coverage
python test command .... python manage.py test
coverage command .... coverage run manage.py test
coverage report command .... coverage report
coverage run --source='social' manage.py test && coverage report && coverage html
'''

class TestPostModel(TestCase):
    def test_post_body(self):
        bodytest = PostTest.objects.create(
            bodytest="django testing", slug="django testing"
        )
        self.assertEqual(str(bodytest), "django testing")

    def test_post_likes(self):
        testuser = User.objects.create_user(
            username="testuser", email="testuser@gmail.com", password="abc123"
        )
        testuser2 = User.objects.create_user(
            username="testuser2", email="testuser2@gmail.com", password="abc123"
        )
        post = PostTest.objects.create(bodytest="test", slug="test")
        post.likestest.set([testuser.pk, testuser2.pk])
        self.assertEqual(post.likestest.count(), 2)

    def test_post_dislikes(self):
        testuser = User.objects.create_user(
            username="testuser", email="testuser@gmail.com", password="abc123"
        )
        testuser2 = User.objects.create_user(
            username="testuser2", email="testuser2@gmail.com", password="abc123"
        )
        post = PostTest.objects.create(bodytest="test", slug="test")
        post.dislikestest.set([testuser.pk, testuser2.pk])
        self.assertEqual(post.dislikestest.count(), 2)
