from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from webhooks.utils import verify_signature


class HasVerifiedSignature(BasePermission):
    def has_permission(self, request: Request, view: View):
        return verify_signature(request)
