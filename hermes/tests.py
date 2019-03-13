from django.http import HttpResponse
from django.test import TestCase
import urllib.request as httprequest
import requests
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

    def test_incoming_voice_call_gather(self):
        result = requests.post(url=self.HOST + 'hermes/voice_call_gather?id=000008830&table_name=company_options',
                               data={'To': '14154171040', 'Digits': 2, 'callSID': 'qwert'})
        print(result.status_code, result.text)

