from django.test import TestCase

from core.models import Convict


# Create your tests here.
class convictTest(TestCase):
    def setUp(self):
        Convict.objects.create(
            name="lion",
            aliases="roar",
            gender="Male",
            date_of_birth="16/05/2023",
            place_of_birth="df",
            place_of_birth_type="Urban",
            education="",
            financial_background="",
            family_record="",
        )

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Convict.objects.get(name="lion")
        self.assertEqual(lion, 'The lion says "roar"')
