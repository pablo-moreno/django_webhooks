from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from webhooks.utils import verify_signature, verify_gitlab_secret


class HasVerifiedSignature(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return verify_signature(request)


class HasGitlabValidSecret(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return verify_gitlab_secret(request)
