from hmac import new as hmac, compare_digest
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def verify_signature(request: Request) -> bool:
    """
        Return whether or not the signature is verified.
        If the GITHUB_SECRET is not specified in app settings,
        it doesn't verify anything and accepts the request.
        This is obviously not recommended for security reasons but
        allows the user not to set it up.
    :param request: Github request
    :return:
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


class AfterResponseAction(Response):
    def __init__(self, *args, **kwargs):
        self.after_response_action = kwargs.get('after_response_action', None)
        kwargs.pop('after_response_action')
        super().__init__(*args, **kwargs)

    def close(self):
        super().close()

        if self.status_code == HTTP_200_OK and callable(self.after_response_action):
            self.after_response_action()
