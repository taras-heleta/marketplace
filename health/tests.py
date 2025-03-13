from django.urls import reverse
from rest_framework.test import APITestCase


class HealthCheckTest(APITestCase):
    def test_healthcheck_endpoint(self):
        url = reverse('healthcheck')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, {"status": "ok"})
