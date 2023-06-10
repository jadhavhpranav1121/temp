from django.db import connections
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


class SQLiteConnectionTest(TestCase):
    def test_sqlite_connection(self):
        connection = connections["default"]
        cursor = connection.cursor()
        cursor.execute("SELECT SQLITE_VERSION()")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 1)  # type: ignore
        cursor.close()
        connection.close()
