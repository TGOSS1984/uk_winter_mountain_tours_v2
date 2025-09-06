from django.test import TestCase, Client
from django.urls import reverse
class CorePagesTests(TestCase):
    def setUp(self): self.client=Client()
    def test_index(self):
        resp=self.client.get(reverse('index'))
        self.assertEqual(resp.status_code,200)
