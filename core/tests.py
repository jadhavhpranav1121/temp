from django.test import TestCase
from django.urls import reverse

from core.models import Convict


# Create your tests here.
class convictTest(TestCase):
    def setUp(self):
        Convict.objects.create(
            name="lion",
            aliases="roar",
            gender="Male",
            date_of_birth="2023-04-15",
            place_of_birth="df",
            place_of_birth_type="Urban",
            education="",
            financial_background="",
            family_record="",
        )

    # def test_animals_can_speak(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Convict.objects.get(name="lion")
    #     self.assertEqual(lion, set())

    def test_whatever_list_view(self):
        lion = Convict.objects.get(name="lion")
        url = "https://localhost:8000/createconvict"
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 301)
        self.assertIn(lion.name, resp.content)
