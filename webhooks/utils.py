from hmac import new as hmac, compare_digest
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def verify_signature(request):
    secret = getattr(settings, 'GITHUB_SECRET').encode()
    signature = request.headers.get('X-Hub-Signature', None)

    if not signature:
        return False

    sha_name, sign = signature.split('=')
    payload = request.body
    mac = hmac(secret, msg=payload, digestmod='sha1').hexdigest()

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
