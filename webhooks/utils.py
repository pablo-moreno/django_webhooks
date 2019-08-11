from hmac import new as hmac, compare_digest
from string import ascii_letters, digits
from random import choice
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def verify_github_signature(request: Request) -> bool:
    """
        Return whether or not the signature is verified.
        If the GITHUB_SECRET is not specified in app settings,
        it doesn't verify anything and accepts the request.
        This is obviously not recommended for security reasons but
        allows the user not to set it up.
    :param request: Github request
    :return: True or False
    """
    secret = getattr(settings, 'GITHUB_SECRET')

    # Does not verify anything and accept the request
    if not secret:
        return True

    signature = request.headers.get('X-Hub-Signature', None)

    if not signature:
        return False

    sha_name, sign = signature.split('=')
    payload = request.body
    mac = hmac(secret.encode(), msg=payload, digestmod='sha1').hexdigest()

    return compare_digest(mac, sign)


def verify_gitlab_secret(request: Request) -> bool:
    """
        Compares X-Gitlab-Token header to GITLAB_SECRET
    :param request:
    :return: True or False
    """
    secret = getattr(settings, 'GITLAB_SECRET')
    gitlab_header = request.headers.get('X-Gitlab-Token', None)

    return gitlab_header == secret


def generate_random_string(char_number):
    return ''.join([
        choice(ascii_letters + digits) for _ in range(0, char_number)
    ])


class AfterResponseAction(Response):
    def __init__(self, *args, **kwargs):
        self.after_response_action = kwargs.pop('after_response_action', None)
        super().__init__(*args, **kwargs)

    def close(self):
        super().close()

        if self.status_code == HTTP_200_OK and callable(self.after_response_action):
            self.after_response_action()
