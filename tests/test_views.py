from django.test import TestCase, Client
from django.urls import reverse
from core.models import Convict, Block


class testViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_convict(self):
        response = self.client.get(reverse("createconvict"))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/createconvict.html")

    def test_block(self):
        response = self.client.get(reverse("createblock"))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, "core/createblock.html")

    def test_blockchain_GET(self):
        response = self.client.get(reverse("get_chain"))
        self.assertEquals(response.status_code, 200)
