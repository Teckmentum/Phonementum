from django.http import HttpResponse
from django.test import TestCase
import urllib.request as httprequest
from hermes import views
# Create your tests here.


class HermesRemoteTestCase(TestCase):

    def setUp(self):
        self.HOST = 'http://127.0.0.1:8000/'

    def test_hermes_up(self):
        result = httprequest.urlopen(self.HOST + 'hermes/greetings').read()
        expected = views.greetings(None)
        # expected = HttpResponse(expected)

        self.assertEqual(result, expected.content, 'Hermes is up')
