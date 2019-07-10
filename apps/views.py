import sys
from io import StringIO
from django.core.management import call_command
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from apps.models import WebHook


class WebhookHandler(APIView):
    def post(self, request):
        webhook = WebHook.from_request(request)
        webhook.save()

        if webhook.type == 'release':
            out = StringIO()
            sys.stdout = out
            call_command('deploy_application', app=webhook.repository, app_version=webhook.version, stdout=out)

        return Response({
            'status': HTTP_200_OK,
        }, status=HTTP_200_OK)
