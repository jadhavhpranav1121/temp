from django.test import SimpleTestCase
from django.urls import reverse, resolve
import core
from core.views import Home


class TestUrls(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url = reverse("home")
        print(url)
        self.assertEqual(resolve(url).func.view_class, Home)
