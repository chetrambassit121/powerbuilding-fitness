from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from members.models import (
    BroadCast_Email,
    City,
    MyAccountManager,
    State,
    User,
    UserProfile,
)


class BaseTest(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="New York")
        self.city = City.objects.create(state=self.state, name="Queens")
        # manually create user
        self.user = User.objects.create(
            email="test@gmail.com",
            username="testuser",
            first_name="chetram",
            last_name="bassit",
            state=self.state,
            city=self.city,
            password="abc123",
        )
        self.user_baker = baker.make(
            User, username="testuser1", state=self.state, city=self.city
        )
        self.email = BroadCast_Email.objects.create(
            subject="testing", message="testing"
        )
        return super().setUp()


class TestState(BaseTest):
    def test_state_str(self):
        state = self.state
        self.assertEqual(str(state), "New York")


class TestCity(BaseTest):
    def test_city_str(self):
        city = self.city
        self.assertEqual(str(city), "Queens")


class TestUser(BaseTest):
    def test_username_str(self):
        username = self.user
        self.assertEqual(str(username), "testuser")


class TestUserBaker(BaseTest):
    def test_username_str(self):
        username = self.user_baker
        self.assertEqual(str(username), "testuser1")


class TestBroadcastEmail(BaseTest):
    def test_subject_str(self):
        subject = self.email
        self.assertEqual(str(subject), "testing")
