from django.test import TestCase
from django.urls import reverse

from members.models import User


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user = {
            "username": "username",
            "email": "nyforchoice@gmail.com",
            "first_name": "chetty",
            "last_name": "bassit",
            "state": "New York",
            "city": "South Richmond Hill",
            "password1": "blacksam101",
            "password2": "blacksam101",
        }
        self.user_short_password = {
            "username": "username",
            "email": "testemail@gmail.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "password1": "tea",
            "password2": "tea",
        }
        self.user_unmatching_password = {
            "username": "username",
            "email": "testemail@gmail.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "password1": "teateas",
            "password2": "teatea",
        }
        self.user_invalid_email = {
            "email": "test.com",
            "username": "username",
            "password": "teslatt",
            "password2": "teslatto",
            "name": "fullname",
        }
        return super().setUp()


class RegisterpageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/members/register/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(response, "registration/register.html")

    def test_template_content(self):
        response = self.client.get(reverse("register"))
        self.assertContains(response, '<h1 style="display: none;">register-test</h1>')
        self.assertNotContains(response, "Not on the page")


class LoginpageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/members/login/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "registration/login.html")

    def test_template_content(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, '<h1 style="display: none;">login-test</h1>')
        self.assertNotContains(response, "Not on the page")

    def test_user_login(self):
        data = {"username": "", "password": "testpassword123"}
        login_url = reverse("login")

        response = self.client.post(login_url, data)
        # resp = response.json()
        self.assertEqual(response.status_code, 200)


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user = {
            "username": "username",
            "email": "nyforchoice@gmail.com",
            "first_name": "chetty",
            "last_name": "bassit",
            "state": "New York",
            "city": "South Richmond Hill",
            "password1": "blacksam101",
            "password2": "blacksam101",
        }
        self.user_short_password = {
            "username": "username",
            "email": "testemail@gmail.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "password1": "tea",
            "password2": "tea",
        }
        self.user_unmatching_password = {
            "username": "username",
            "email": "testemail@gmail.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "password1": "teateas",
            "password2": "teatea",
        }
        self.user_invalid_email = {
            "email": "test.com",
            "username": "username",
            "password": "teslatt",
            "password2": "teslatto",
            "name": "fullname",
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 200)
 