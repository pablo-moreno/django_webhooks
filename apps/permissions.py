import json
import logging
from hmac import new as hmac, compare_digest
from django.conf import settings
from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

logger = logging.getLogger('webhooks')


class HasVerifiedSignature(BasePermission):
    def has_permission(self, request: Request, view: View):
        secret = getattr(settings, 'GITHUB_SECRET').encode()
        signature = request.headers.get('X-Hub-Signature', None)

        if not signature:
            return False

        sha_name, sign = signature.split('=')
        payload = request.body
        mac = hmac(secret, msg=payload, digestmod='sha1').hexdigest()

        logger.info(f'mac: {mac}')
        logger.info(f'sign: {sign}')

        return compare_digest(mac, sign)
