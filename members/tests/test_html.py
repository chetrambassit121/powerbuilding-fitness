from django.test import TestCase
from django.urls import reverse

from members.models import User


class RegisterHtmlTest(TestCase):
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


class LoginHtmlTest(TestCase):
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
