from django.test import TestCase, Client
from django.urls import reverse


class MainTest(TestCase):
    ru_headers = {"Accept-Language": "ru"}
    en_headers = {"Accept-Language": "en"}

    def setUp(self):
        self.client = Client()
        self.main_url = reverse('main')

    def test_main_page_status(self):
        response = self.client.get(self.main_url)
        self.assertEquals(response.status_code, 200)

    def test_ru_content(self):
        response = self.client.get(self.main_url, headers=self.ru_headers)
        self.assertIn("Привет от Хекслета!", str(response._container[0].decode('utf-8')))
        self.assertEquals(response.headers.get("Content-Language"), "ru")

    def test_en_content(self):
        response = self.client.get(self.main_url, headers=self.en_headers)
        self.assertIn("Hello from Hexlet", str(response._container[0].decode('utf-8')))
        self.assertEquals(response.headers.get("Content-Language"), "en-us")
