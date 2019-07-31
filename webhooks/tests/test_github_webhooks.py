import os
import json
from rest_framework.test import APITestCase
from webhooks.models import Application

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_FIXTURE = os.path.join(BASE_DIR, 'fixtures', 'github.json')


def get_github_fixture():
    with open(GITHUB_FIXTURE) as f:
        response = f.read()
    return json.loads(response)


class TestGithubWebhooks(APITestCase):
    def setUp(self):
        self.body = get_github_fixture()
        self.application = Application(
            name='Github Webhooks',
            repository='https://github.com/pablo-moreno/github_webhooks',
            deploy_script=os.path.join(BASE_DIR, 'scripts', 'script.sh'),
            version='1.0.0'
        )
        self.application.save()
        self.fixture = get_github_fixture()
        self.headers = {
            'HTTP_X_GITHUB_EVENT': 'release'
        }

    def test_github_webhook_response_200(self):
        response = self.client.post('/', data=self.fixture, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_executes_deploy_script(self):
        response = self.client.post('/', data=self.fixture, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        with open('test.txt') as f:
            file_content = f.read()

        self.assertEqual(file_content, 'Hello, Webhook\n')

    def tearDown(self):
        if os.path.isfile('test.txt'):
            os.remove('test.txt')
