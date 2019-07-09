from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.core.management import call_command
from apps.models import WebHook


class WebhookHandler(APIView):
    def post(self, request):
        webhook = WebHook.from_request(request)
        webhook.save()

        if webhook.type == 'release':
            result = call_command('deploy_application', app=webhook.url)
            print(result)

        return Response(status=HTTP_200_OK)
