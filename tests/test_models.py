from django.test import TestCase
from core.models import Convict, Block


class testModels(TestCase):
    def setUp(self):
        self.Convict1 = Convict.objects.create(
            name="Pranav Jadhav",
            aliases="Prony",
            gender="Male",
            place_of_birth="Bhigwan",
            place_of_birth_type="Rural",
            date_of_birth="2023-12-01",
            education="graduate",
            financial_background="middle",
            family_record="good",
        )

    def test_convict_models(self):
        self.assertEquals(self.Convict1.name, "Pranav Jadhav")
