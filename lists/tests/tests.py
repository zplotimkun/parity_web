from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.utils.importlib import import_module
from django.template.loader import render_to_string

from lists.views import home_page

# Create your tests here.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Tim parity web</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))