import sys
from io import StringIO
from django.core.management import call_command
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from apps.models import WebHook
from apps.utils import AfterResponseAction


class WebhookHandler(APIView):
    def release(self, webhook):
        def run_command():
            out = StringIO()
            sys.stdout = out
            call_command('deploy_application', app=webhook.repository, app_version=webhook.version, stdout=out)
        return run_command

    def post(self, request):
        webhook = WebHook.from_request(request)
        webhook.save()

        if webhook.type == 'release' and webhook.action == 'published':
            return AfterResponseAction({
                'status': HTTP_200_OK,
            }, after_response_action=self.release(webhook))

        return Response({
            'status': HTTP_200_OK,
        }, status=HTTP_200_OK)
